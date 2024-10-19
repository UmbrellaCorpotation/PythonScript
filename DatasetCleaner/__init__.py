import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import requests
import logging

def cargar_y_limpiar_datos(ruta_csv, umbral_columnas=0.5, metodo_relleno='mean'):
    # Cargar datos
    df = pd.read_csv(ruta_csv)
    logging.info(f"Datos cargados correctamente. Forma inicial: {df.shape}")

    # Mostrar información inicial
    logging.debug(f"Columnas iniciales: {df.columns.tolist()}")
    logging.debug(f"Tipos de datos:\n{df.dtypes}")
    logging.debug(f"Valores nulos por columna:\n{df.isnull().sum()}")

    # Eliminar columnas con más del umbral de valores nulos
    df = df.loc[:, df.isnull().mean() < umbral_columnas]
    logging.info(f"Columnas después de eliminar las que tienen más del {umbral_columnas*100}% de valores nulos: {df.columns.tolist()}")

    # Rellenar valores nulos en columnas numéricas
    imputer = SimpleImputer(strategy=metodo_relleno)
    columnas_numericas = df.select_dtypes(include=[np.number]).columns
    if not columnas_numericas.empty:
        df[columnas_numericas] = imputer.fit_transform(df[columnas_numericas])
        logging.info(f"Valores nulos en columnas numéricas rellenados usando el método '{metodo_relleno}'.")
    else:
        logging.info("No se encontraron columnas numéricas para rellenar.")

    # Eliminar filas con valores nulos restantes
    df.dropna(inplace=True)
    logging.info(f"Forma después de eliminar filas con valores nulos: {df.shape}")

    # Eliminar filas duplicadas
    df.drop_duplicates(inplace=True)
    logging.info(f"Forma después de eliminar filas duplicadas: {df.shape}")

    # Normalizar nombres de columnas
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    logging.info(f"Nombres de columnas normalizados: {df.columns.tolist()}")

    # Renombrar columnas para que coincidan con los nombres esperados por el backend
    df.rename(columns={
        'name': 'name',
        'category': 'category',
        'dosage_form': 'dosageForm',
        'strength': 'strength',
        'manufacturer': 'manufacturer',
        'indication': 'indication',
        'classification': 'classification'
    }, inplace=True)

    return df

def enviar_datos_api(df, url_api, tipo, tamano_lote=100):
    total_registros = len(df)
    headers = {'Content-Type': 'application/json'}
    logging.info(f"Enviando un total de {total_registros} registros a la API.")

    for inicio in range(0, total_registros, tamano_lote):
        fin = min(inicio + tamano_lote, total_registros)
        lote = df.iloc[inicio:fin].to_dict(orient='records')
        try:
            # Construir la URL correcta sin duplicar '/batch'
            url_con_tipo = f"{url_api}/batch/{tipo}"
            # Enviar el lote al endpoint correcto
            respuesta = requests.post(url_con_tipo, json=lote, headers=headers)
            if respuesta.status_code in (200, 201):
                logging.info(f"Lote {inicio + 1}-{fin} enviado correctamente.")
            else:
                logging.error(f"Error al enviar lote {inicio + 1}-{fin}: {respuesta.status_code} - {respuesta.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Excepción al enviar lote {inicio + 1}-{fin}: {e}")

if __name__ == "__main__":
    # Configuración del registro de logs
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Definir las rutas y parámetros directamente en el script
        ruta_csv = "C:/Users/cuell/OneDrive/Documentos/GitHub/PythonScript/medicine_dataset.csv"  # <-- Modifica esta ruta con la ubicación de tu archivo CSV
        url_api = "http://localhost:8080/api/muestras"  # <-- Modifica esta URL con la de tu backend
        tipo = "bioquimico"
        umbral_columnas = 0.5
        metodo_relleno = 'mean'  # Opciones: 'mean', 'median', 'most_frequent'
        tamano_lote = 100
        ruta_salida = "C:/Users/cuell/OneDrive/Documentos/GitHub/PythonScript/datasetLimpio.csv"  # <-- Opcional: especifica una ruta si deseas guardar el CSV limpio

        # Cargar y limpiar datos
        df_limpio = cargar_y_limpiar_datos(
            ruta_csv=ruta_csv,
            umbral_columnas=umbral_columnas,
            metodo_relleno=metodo_relleno
        )

        # Guardar CSV limpio si se proporciona una ruta de salida
        if ruta_salida:
            df_limpio.to_csv(ruta_salida, index=False)
            logging.info(f"Datos limpios guardados en {ruta_salida}")

        # Enviar datos a la API REST
        enviar_datos_api(df_limpio, url_api, tipo, tamano_lote=tamano_lote)

    except Exception as e:
        logging.error(f"Se produjo un error: {e}")