import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import json
import requests

# Función para limpiar el dataset
def clean_data(csv_path):
    df = pd.read_csv(csv_path)

    # Mostrar información del dataset antes de la limpieza
    print("Información del DataFrame antes de la limpieza:")
    print(df.info())
    print(df.head())

    # Limpiar valores nulos para las columnas numéricas
    imputer = SimpleImputer(strategy='mean')

    # Seleccionar solo las columnas numéricas (en tu caso no hay, pero es un ejemplo)
    if not df.select_dtypes(include=[np.number]).empty:
        df[df.select_dtypes(include=[np.number]).columns] = imputer.fit_transform(df.select_dtypes(include=[np.number]))
    else:
        print("No se encontraron columnas numéricas en el dataset.")

    # Devolver el DataFrame limpio
    return df

# Convertir el dataset limpio a JSON y enviar al backend
def send_to_backend(df, backend_url):
    # Convertir el DataFrame a JSON
    data_json = df.to_json(orient='records')

    # Mostrar los primeros registros del JSON convertido
    print("Datos en formato JSON:")
    print(data_json[:500])  # Mostramos una parte del JSON (puede ser muy grande)

    # Hacer una petición POST al backend
    response = requests.post(backend_url, json=json.loads(data_json))

    # Verificar si la petición fue exitosa
    if response.status_code == 201:
        print(f"Datos enviados correctamente al backend: {backend_url}")
    else:
        print(f"Error al enviar datos al backend. Código de estado: {response.status_code}")

if __name__ == "__main__":
    # Ruta del CSV original y la URL del backend
    csv_path = "C:/Users/cuell/OneDrive/Documentos/GitHub/PythonScript/medicine_dataset.csv"
    backend_url = 'http://localhost:8080/api/datos-bioquimicos'

    # Limpiar el dataset
    df_cleaned = clean_data(csv_path)

    # Enviar el dataset limpio al backend en formato JSON
    send_to_backend(df_cleaned, backend_url)
