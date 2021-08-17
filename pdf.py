import json
from re import escape
from fpdf import FPDF

json_compra_oro = r"C:\raisa-bruker\files\compra_oro.json"
json_compra_plata = r"C:\raisa-bruker\files\compra_plata.json"

pdf_compras = r"C:\raisa-bruker\impresiones\compras"


def impresion_compra(n_compra, tipo_compra, total_compra):
    # Instancia de FPDF class
    pdf = FPDF(format='letter', unit='in')

    # Se agrega una página, sino, no se crea el documento
    pdf.add_page()

    # Fuente del documento
    pdf.set_font('Times', '', 10.0)

    # Espacio "efectivo" de la página -> ancho total menos el espacio de los margenes
    espacio_efectivo = pdf.w - 2*pdf.l_margin

    # Cargo el archivo json de las respectivas compras
    if tipo_compra == "Oro":
        with open(json_compra_oro) as fichero_compra_oro:
            piezas_compradas = json.load(fichero_compra_oro)
    
    if tipo_compra == "Plata":
        with open(json_compra_plata) as fichero_compra_plata:
            piezas_compradas = json.load(fichero_compra_plata)
    
    # Número de columnas
    n_columnas = 4

    # Calculo del ancho de las columnas
    ancho_columna = espacio_efectivo/n_columnas

    # Nombre de los encabezados
    nombre_encabezados = ["Descripcion", "Aleacion", "Peso", "Precio"]

    # Datos de la compra inicializada como una lista vacía
    datos = []
    datos.append(nombre_encabezados)

    # Agregamos los datos de la compra
    for pieza in piezas_compradas:
        datos_pieza = []
        datos_pieza.append(pieza["Descripcion"])
        datos_pieza.append(pieza["Aleacion"])
        datos_pieza.append("{}g".format(float(pieza["Peso"])))
        datos_pieza.append("$ {}".format(float(pieza["Precio_ingresado"])))

        datos.append(datos_pieza)
    
    print(datos)

    pdf.ln(0.5)

    # Título de la tabla
    pdf.set_font('Times', 'B', 14.0)
    pdf.cell(espacio_efectivo, 0.0, "Compra #{}".format(n_compra), align='C')
    pdf.set_font('Times', '', 10.0)
    pdf.ln(0.4)

    # Altura del texto
    altura_texto = pdf.font_size

    # Escritura de la tabla
    for fila in datos:
        for dato in fila:
            pdf.cell(ancho_columna, altura_texto*2, str(dato), border=1, align='C')

        pdf.ln(altura_texto*2)

    pdf.ln(0.4)

    total = ["", "", "TOTAL:", "$ {}".format(float(total_compra))]

    pdf.set_font('Times', '', 12.0)
        
    for dato in total:
        pdf.cell(ancho_columna, altura_texto, str(dato), border=0, align='C')
    pdf.ln(altura_texto)
    

    pdf.output(pdf_compras + "/" + "Compra #{} - {}.pdf".format(n_compra, tipo_compra))

# impresion_compra(2, "Plata", 65.54)