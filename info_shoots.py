import os
from os import remove

import pandas as pd

# Rutas 
csv_results = r"C:\raisa-bruker\disparos\Results.csv"
json_results = r"C:\raisa-bruker\files\results.json"

def limpiar_results():
    df_results = pd.read_csv(csv_results)

    # Columnas a utilizar
    columnas = []
    columnas_comunes = [
        "File #", "DateTime", "Operator",
        "Application", "Method", "Alloy 1"
    ]

    # Elementos a destacar
    # joyeria = ["Au", "Ag", "Cu", "Zn", "Pt", "Pd", "Rh", "Ru", "Fe", "Rh"]
    # contaminantes = ["Sn", "Pb", "Ni", "W"]

    elementos_destacados = ["Au", "Ag", "Cu", "Zn", "Pt", "Pd", "Rh", "Ru", "Fe", "Rh",
                            "Sn", "Pb", "Ni", "W"]

    # Copia del dataframe para trabajar
    df_copia_results = df_results.copy()

    # Obtiene las columnas del dataframe copia de results
    encabezado = df_copia_results.columns
    elementos = encabezado.intersection(elementos_destacados)

    # Obtiene la lista completa de las columnas comunes (las de todos los archivos) + la lista de elementos que se encuentran en ese dataframe
    columnas = list(columnas_comunes) + list(elementos)

    # Dataframe limpio
    df_limpio = df_copia_results[columnas]
    df_limpio = df_limpio.fillna(0)
    df_limpio = df_limpio.replace({"< LOD": 0.0})

    df_limpio.to_json(json_results, orient="records")
    
# limpiar_results(csv_results)