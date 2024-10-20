# Script de Carga, Limpieza y Envío de Datos

Este script de Python tiene como objetivo cargar un conjunto de datos desde un archivo CSV, limpiarlo y enviarlo en lotes a un backend a través de una API REST. Está diseñado para ser flexible, permitiendo configurar ciertos parámetros, como la estrategia de imputación para los valores nulos y el tamaño del lote para el envío de los datos.

## 1. Funcionalidades

El script realiza las siguientes acciones:

1. **Carga de Datos**: Lee un archivo CSV que contiene datos de muestras o medicamentos.
2. **Limpieza de Datos**:
   - Elimina columnas con demasiados valores nulos.
   - Rellena los valores nulos restantes en columnas numéricas usando una estrategia configurable (`mean`, `median`, `most_frequent`).
   - Elimina filas duplicadas.
   - Normaliza los nombres de las columnas.
3. **Renombrado de Columnas**: Renombra las columnas para que coincidan con las convenciones esperadas por el backend.
4. **Envío a la API**: Envía los datos procesados a una API en lotes para mejorar el rendimiento y evitar saturar el servidor con grandes cantidades de datos en una única petición.
5. **Logging**: Registra toda la actividad del proceso para facilitar la depuración y el monitoreo.

## 2. Requisitos

- **Python 3.x**
- **Pandas** para la manipulación de datos.
- **Numpy** para operaciones numéricas.
- **Scikit-learn** para el procesamiento de datos (imputación de valores nulos).
- **Requests** para realizar peticiones HTTP a la API REST.

Instalación de dependencias:

```bash
pip install pandas numpy scikit-learn requests
