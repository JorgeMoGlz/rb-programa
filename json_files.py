import os
import json

import info_shoots

json_oro = r"C:\raisa-bruker\files\precios_oro.json"
json_plata = r"C:\raisa-bruker\files\precios_plata.json"

json_compra_oro = r"C:\raisa-bruker\files\compra_oro.json"
json_compra_plata = r"C:\raisa-bruker\files\compra_plata.json"
json_compra = r"C:\raisa-bruker\files\compra.json"

json_results = r"C:\raisa-bruker\files\results.json"

def precios_oro(precio_oro):

    if os.path.exists(json_oro):
        os.remove(json_oro)

    kilataje = ["24K", "23K", "22K", "21K", "20K",
                "19K", "18K", "17K", "16K", "15K",
                "14K", "13K", "12K", "11K", "10K",
                "9K", "8K", "7K", "6K"]

    porcentaje = [100.00, 95.75, 91.00, 87.42, 83.25,
                  79.09, 75.00, 69.00, 65.00, 62.42,
                  58.30, 53.50, 48.00, 45.00, 41.50,
                  37.00, 31.00, 27.00, 23.00]

    precios = []

    for p in porcentaje:
        if p == 99.90:
            precios.append(precio_oro)
        else:
            precios.append(round((p*precio_oro)/100.00, 2))
    
    dict_precios = []
    
    for i in range(len(precios)):
        dict_precios.append({
            "Pureza": kilataje[i],
            "Porcentaje": str(porcentaje[i]),
            "Precio": str(precios[i])
        })
    
    with open(json_oro, 'w') as fichero_oro:
        json.dump(dict_precios, fichero_oro)

def precios_plata(precio_plata):
    if os.path.exists(json_plata):
        os.remove(json_plata)

    ley = ["Ley 999", "Ley 950", "Ley 935", "Ley 925", "Ley 835"]

    porcentaje = [99.99, 95.00, 93.50, 92.50, 83.50]

    precios = []

    for p in porcentaje:
        if p == 99.99:
            precios.append(precio_plata)
        else:
            precios.append(round((p*precio_plata)/100.00, 2))
    

    dict_precios = []
    
    for i in range(len(precios)):        
        dict_precios.append({
            "Pureza": ley[i],
            "Porcentaje": str(porcentaje[i]),
            "Precio": str(precios[i])
        })

    with open(json_plata, 'w') as fichero_plata:
        json.dump(dict_precios, fichero_plata)

# def compra_oro(descripcion, peso, aleacion, porcentaje, precio_ingresado, precio_real):
def compra_oro(descripcion, peso, aleacion, porcentaje, precio_real):
    # precio_ingresado = "{:.2f}".format(float(precio_ingresado))
    
    precio_calculado = (float(precio_real)*float(peso))
    precio_calculado = "{:.2f}".format(precio_calculado)
    
    peso = "{:.2f}".format((float(peso)*float(porcentaje))/100)

    if not os.path.exists(json_compra_oro):
        compras_oro = []
    else:
        with open(json_compra_oro) as fichero_compra_oro:
            compras_oro = json.load(fichero_compra_oro)

    compras_oro.append({
        "Descripcion": descripcion,
        "Aleacion": aleacion,
        # "Peso": peso,
        "Peso_puro": peso,
        "Precio": precio_calculado,
        # "Precio_ingresado": precio_ingresado
    })

    with open(json_compra_oro, 'w') as fichero_compra_oro:
        json.dump(compras_oro, fichero_compra_oro)

#def compra_plata(descripcion, peso, aleacion, porcentaje, precio_ingresado, precio_real):
def compra_plata(descripcion, peso, aleacion, porcentaje, precio_real):
    # precio_ingresado = "{:.2f}".format(float(precio_ingresado))

    precio_calculado = (float(precio_real)*float(peso))
    precio_calculado = "{:.2f}".format(precio_calculado)

    peso = "{:.2f}".format((float(peso)*float(porcentaje))/100)

    if not os.path.exists(json_compra_plata):
        compras_plata = []
    else:
        with open(json_compra_plata) as fichero_compra_plata:
            compras_plata = json.load(fichero_compra_plata)

    compras_plata.append({
        "Descripcion": descripcion,
        "Aleacion": aleacion,
        # "Peso": peso,
        "Peso_puro": peso,
        "Precio": precio_calculado,
        # "Precio_ingresado": precio_ingresado
    })

    with open(json_compra_plata, 'w') as fichero_compra_plata:
        json.dump(compras_plata, fichero_compra_plata)

def compra(descripcion, peso, aleacion, porcentaje, precio_ingresado, precio_real):
    precio_ingresado = "{:.2f}".format(float(precio_ingresado))

    precio_calculado = (float(precio_real)*float(peso))
    precio_calculado = "{:.2f}".format(precio_calculado)

    peso = "{:.2f}".format((float(peso)*float(porcentaje))/100)

    if not os.path.exists(json_compra):
        compras = []
    else:
        with open(json_compra) as fichero_compra:
            compras = json.load(fichero_compra)

    compras.append({
        "Descripcion": descripcion,
        "Aleacion": aleacion,
        "Peso": peso,
        "Precio_calculado": precio_calculado,
        "Precio_ingresado": precio_ingresado
    })

    with open(json_compra, 'w') as fichero_compra:
        json.dump(compras, fichero_compra)

def datos_results():
    info_shoots.limpiar_results()
    
    with open(json_results) as fichero_results:
        registros_results = json.load(fichero_results)

    conjunto_joyeria = set(["Alloy 1", "Au", "Ag", "Cu", "Zn", "Pt", "Pd", "Rh", "Ru", "Fe", "Rh"])
    conjunto_contaminantes = set(["Sn", "Pb", "Ni", "W"])

    keys_results = list(registros_results[0].keys())

    conjunto_keys_results = set(keys_results)

    joyeria_igual = list(conjunto_joyeria & conjunto_keys_results)
    contaminantes_iguales = list(conjunto_contaminantes & conjunto_keys_results)

    datos_joyeria = {}
    datos_contaminantes = {}

    for registro in registros_results:
        for elemento in joyeria_igual:
            if registro[elemento] != 0.0:
                datos_joyeria[elemento] = registro[elemento]

        for elemento in contaminantes_iguales:
            if registro[elemento] != 0.0:
                datos_contaminantes[elemento] = registro[elemento]

    if datos_joyeria["Alloy 1"] == "No Match":
        if datos_joyeria.get("Au") != None:
            datos_joyeria["Alloy 1"] = "{} %".format(int((round(float(datos_joyeria["Au"]), 0)) * 10))
        if datos_joyeria.get("Ag") != None:
            datos_joyeria["Alloy 1"] = "Ley {}".format(int((round(float(datos_joyeria["Ag"]), 0)) * 10))

    return [datos_joyeria, datos_contaminantes]

# datos_results()