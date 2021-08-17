import os
import json

json_oro = r"C:\raisa-bruker\files\precios_oro.json"
json_plata = r"C:\raisa-bruker\files\precios_plata.json"

json_compra_oro = r"C:\raisa-bruker\files\compra_oro.json"
json_compra_plata = r"C:\raisa-bruker\files\compra_plata.json"

def precios_oro(precio_oro):

    if os.path.exists(json_oro):
        os.remove(json_oro)

    kilataje = ["24K", "23K", "22K", "21K", "20K",
                "19K", "18K", "17K", "16K", "15K",
                "14K", "13K", "12K", "11K", "10K",
                "9K", "8K", "7K", "6K"]

    porcentaje = [99.90, 95.75, 91.59, 87.42, 83.25,
                  79.09, 74.92, 70.75, 66.59, 62.42,
                  58.26, 54.09, 49.92, 45.76, 41.59,
                  37.42, 33.26, 29.09, 24.93]

    precios = []

    for p in porcentaje:
        if p == 99.90:
            precios.append(precio_oro)
        else:
            precios.append(round((p*precio_oro)/99.90, 2))
    
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

    ley = ["Ley 999", "Ley 950", "Ley 925", "Ley 835"]

    porcentaje = [99.90, 95.00, 92.50, 83.50]

    precios = []

    for p in porcentaje:
        if p == 99.90:
            precios.append(precio_plata)
        else:
            precios.append(round((p*precio_plata)/99.90, 2))

    dict_precios = []
    
    for i in range(len(precios)):
        dict_precios.append({
            "Pureza": ley[i],
            "Porcentaje": str(porcentaje[i]),
            "Precio": str(precios[i])
        })

    with open(json_plata, 'w') as fichero_plata:
        json.dump(dict_precios, fichero_plata)

def compra_oro(descripcion, peso, aleacion, porcentaje, precio_ingresado, precio_real):
    precio_ingresado = "{:.2f}".format(float(precio_ingresado))
    
    precio_calculado = (float(precio_real)*float(peso))
    precio_calculado = "{:.2f}".format(precio_calculado)

    if not os.path.exists(json_compra_oro):
        compras_oro = []
    else:
        with open(json_compra_oro) as fichero_compra_oro:
            compras_oro = json.load(fichero_compra_oro)

    compras_oro.append({
        "Descripcion": descripcion,
        "Aleacion": aleacion,
        "Peso": peso,
        "Precio_calculado": precio_calculado,
        "Precio_ingresado": precio_ingresado
    })

    with open(json_compra_oro, 'w') as fichero_compra_oro:
        json.dump(compras_oro, fichero_compra_oro)

def compra_plata(descripcion, peso, aleacion, porcentaje, precio_ingresado, precio_real):
    precio_ingresado = "{:.2f}".format(float(precio_ingresado))

    precio_calculado = (float(precio_real)*float(peso))
    precio_calculado = "{:.2f}".format(precio_calculado)

    if not os.path.exists(json_compra_plata):
        compras_plata = []
    else:
        with open(json_compra_plata) as fichero_compra_plata:
            compras_plata = json.load(fichero_compra_plata)

    compras_plata.append({
        "Descripcion": descripcion,
        "Aleacion": aleacion,
        "Peso": peso,
        "Precio_calculado": precio_calculado,
        "Precio_ingresado": precio_ingresado
    })

    with open(json_compra_plata, 'w') as fichero_compra_plata:
        json.dump(compras_plata, fichero_compra_plata)



    
    
        


