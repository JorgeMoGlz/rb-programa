import os
import sys
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from datetime import datetime

import db, formats, json_files, pdf

# Rutas generales
json_oro = r"C:\raisa-bruker\files\precios_oro.json"
json_plata = r"C:\raisa-bruker\files\precios_plata.json"

json_compra_oro = r"C:\raisa-bruker\files\compra_oro.json"
json_compra_plata = r"C:\raisa-bruker\files\compra_plata.json"

foto_pieza = r"C:\raisa-bruker\foto"

class Caja(QLabel):
    def __init__(self, texto="", fuente="Arial", tam=16, color="", alV=Qt.AlignVCenter, alH=Qt.AlignHCenter):
        super().__init__()

        self.setStyleSheet(f"background-color:{color}")
        self.setText(texto)
        font = QFont(fuente, tam)
        self.setFont(font)
        self.setAlignment(alH | alV)

class VentanaConsultas(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Consultas")
        self.showMaximized()

        # Layout principal
        layout_principal = QVBoxLayout()

        # Layouts secundarios
        layout_encabezado = QHBoxLayout()
        layout_calendario = QHBoxLayout()
        layout_fechas = QHBoxLayout()
        layout_consultar = QHBoxLayout()
        layout_informacion = QHBoxLayout()

        # Agregar layouts secundarios al principal
        layout_principal.addLayout(layout_encabezado)
        layout_principal.addLayout(layout_calendario)
        layout_principal.addLayout(layout_fechas)
        layout_principal.addLayout(layout_consultar)
        layout_principal.addLayout(layout_informacion)

        ############################## WIDGETS ##############################
        # Widgets del layout encabezado
        label_titulo = Caja("Selecciona las fechas", "Arial")

        # Widgets del layout calendario
        calendar_1 = QCalendarWidget()
        calendar_1.setGridVisible(True)
        calendar_1.clicked.connect(self.fecha_inicial)

        calendar_2 = QCalendarWidget()
        calendar_2.setGridVisible(True)
        calendar_2.clicked.connect(self.fecha_final)

        # Widgets del layout fechas
        self.label_fecha_1 = Caja("Fecha inicial", "Arial")
        self.label_fecha_2 = Caja("Fecha final", "Arial")

        # Widgets del layout consultar
        button_consultar = QPushButton("Consultar compras")
        button_consultar.clicked.connect(self.consultar)

        # Widgets del layout información
        self.table_consulta = QTableWidget()
        self.labels_encabezado = ["pieza", "porcentaje", "aleacion", "peso", "precio_calculado", "precio_cliente"]
        self.table_consulta.setColumnCount(len(self.labels_encabezado))
        self.table_consulta.setHorizontalHeaderLabels(self.labels_encabezado)

        #####################################################################

        # Agregar widgets a los respectivos layouts
        layout_encabezado.addWidget(label_titulo)
        
        layout_calendario.addWidget(calendar_1)
        layout_calendario.addWidget(calendar_2)

        layout_fechas.addWidget(self.label_fecha_1)
        layout_fechas.addWidget(self.label_fecha_2)

        layout_consultar.addWidget(button_consultar)

        layout_informacion.addWidget(self.table_consulta)

        # Agregar layout principal a la ventana
        self.setLayout(layout_principal)

        # Atributo para cerrar todas las ventanas al cerrar la ventana principal
        self.setAttribute(Qt.WA_QuitOnClose, False)
    
    def fecha_inicial(self, date):
        self.fecha_1 = formats.format_stringdate(date.toString())
        self.label_fecha_1.setText(self.fecha_1)
        print(formats.format_stringdate(date.toString()))
    
    def fecha_final(self, date):
        self.fecha_2 = formats.format_stringdate(date.toString())
        self.label_fecha_2.setText(self.fecha_2)
        print(formats.format_stringdate(date.toString()))

    def consultar(self):
        json_files.consulta(self.fecha_1, self.fecha_2)

class VentanaVentas(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Venta de analisis")
        self.setMinimumSize(700, 360)

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(10)

        # Variables generales
        self.foto_actual = ""
        self.elementos_joyeria = ""
        self.elementos_contaminantes = ""

        # Layouts secundarios
        layout_encabezado = QHBoxLayout()
        layout_obtenerinfo = QHBoxLayout()
        layout_informacion = QHBoxLayout()
        layout_confirmar = QHBoxLayout()

        # Layouts terciarios
        layout_datos = QVBoxLayout()

        # Agregar layouts secundarios al principal
        layout_principal.addLayout(layout_encabezado)
        layout_principal.addLayout(layout_obtenerinfo)
        layout_principal.addLayout(layout_informacion)
        layout_principal.addLayout(layout_confirmar)
        
        ############################## WIDGETS ##############################
        # Widgets del layout encabezado
        label_titulo = Caja("Analisis", "Arial")

        # Widgets del layout obtenerinfo
        button_foto = QPushButton("Información del disparo")
        button_foto.clicked.connect(self.obtener_foto)
        
        button_info = QPushButton("Obtener información del disparo")
        button_info.clicked.connect(self.obtener_info)

        # Widgets del layout informacion
        self.label_foto = Caja()
        foto = QPixmap(r"C:\raisa-bruker\images\imagen-vacia.jpg").scaled(QSize(50, 50))
        self.label_foto.setPixmap(foto)
        self.label_foto.setScaledContents(True)

        # Widgets del layout datos
        self.label_aleacion = Caja("Aleacion\n1")
        self.label_joyeria = Caja("Elementos de interés\n2")
        self.label_contaminantes = Caja("Contaminantes\n3")

        # Widgets del layout confirmar
        button_confirmar = QPushButton("Confirmar compra")
        button_confirmar.clicked.connect(self.confirmar)

        #####################################################################

        # Agregar widgets a los respectivos layouts
        layout_encabezado.addWidget(label_titulo)
        
        layout_obtenerinfo.addWidget(button_foto)
        layout_obtenerinfo.addWidget(button_info)

        layout_informacion.addWidget(self.label_foto)
        layout_informacion.addLayout(layout_datos)
        layout_datos.addWidget(self.label_aleacion)
        layout_datos.addWidget(self.label_joyeria)
        layout_datos.addWidget(self.label_contaminantes)

        layout_confirmar.addWidget(button_confirmar)

        # Agregar layout principal a la ventana
        self.setLayout(layout_principal)
        
        # Atributo para cerrar todas las ventanas al cerrar la ventana principal
        self.setAttribute(Qt.WA_QuitOnClose, False)

    def obtener_foto(self):
        print("Foto obtenida")
        f = [arch.name for arch in os.scandir(foto_pieza) if arch.is_file()][0]

        self.foto_actual = foto_pieza + "/" + f
        nueva_foto = QPixmap(foto_pieza + "/" + f).scaled(QSize(50, 50))

        self.label_foto.setPixmap(nueva_foto)

        print(self.foto_actual)
    
    def obtener_info(self):
        joyeria, contaminantes = json_files.datos_results()
        self.label_aleacion.setText(joyeria["Alloy 1"])
        
        joy = []
        cont = []
        
        for key in joyeria:
            if key == "Alloy 1":
                pass
            else:
                joy.append("{}: {}".format(key, round(float(joyeria[key]), 2)))
        
        for key in contaminantes:
            if key == "Alloy 1":
                pass
            else:
                cont.append("{}: {}".format(key, round(float(contaminantes[key]), 2)))
        
        if len(joy) == 0:
            info_joy = "Sin elementos de joyeria"
        else:
            info_joy = ' '.join([str(elem) for elem in joy])

        if len(cont) == 0:
            info_cont = "Sin elementos contaminantes"
        else:
            info_cont = ' '.join([str(elem) for elem in cont])

        self.elementos_joyeria = info_joy
        self.elementos_contaminantes = info_cont

        self.label_joyeria.setText(info_joy)
        self.label_contaminantes.setText(info_cont)

        print(self.elementos_contaminantes)
        print(self.elementos_joyeria)

    def confirmar(self):
        pdf.impresion_venta(self.foto_actual, self.elementos_joyeria, self.elementos_contaminantes)
        print("PDF creado")

class VentanaCompras(QWidget):
    def __init__(self):
        super().__init__()

        ################## Variables generales #####################
        # Variable de selección del elemento que se comprará
        self.elemento = "Oro"
        self.peso_pieza = 0
        self.precio_ingresado = 0
        # Variable del precio registrado
        self.precio = 0
        self.total = 0

        # Variable para saber si una compra es por lote
        self.descripcion_pieza = "Pieza de lote"

        # Variable para saber la aleacion
        self.aleacion = "24K"

        # Variable para saber si es una compra nueva
        self.nueva_compra = True

        # Creación de la compra
        self.id_oro, act_oro, self.precio_oro = db.ultimo_precio_oro()[0]
        self.id_plata, act_plata, self.precio_plata = db.ultimo_precio_plata()[0]

        if self.elemento == "Oro":
            self.precio = self.precio_oro
        ############################################################
        
        if len(db.ultima_compra()) == 0:
            datos_compra = [0, 0, self.id_oro, self.id_plata]
            db.crear_compra(datos_compra)

        if db.ultima_compra()[0][2] != 0.0:
            datos_compra = [0, 0, self.id_oro, self.id_plata]
            db.crear_compra(datos_compra)
        
        self.id_compra, fecha_compra, precio_calculado, precio_compra, self.id_oro, self.id_plata = db.ultima_compra()[0]

        # Datos del archivo json
        with open(json_oro) as fichero_oro:
            self.datos_oro = json.load(fichero_oro)
        
        with open(json_plata) as fichero_plata:
            self.datos_plata = json.load(fichero_plata)
        
        # Variable porcentaje
        self.porcentaje = self.datos_oro[0]["Porcentaje"]

        # Configuración de la ventana
        self.setWindowTitle("Compra de piezas")
        self.setMinimumSize(600, 500)

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(10)

        # Layouts secundarios
        layout_encabezado = QHBoxLayout()
        layout_seleccion = QHBoxLayout()
        layout_datos = QHBoxLayout()
        layout_obtenerinfo = QHBoxLayout()
        layout_datoscompra = QHBoxLayout()
        layout_total = QHBoxLayout()
        layout_confirmacion = QHBoxLayout()

        # Agregar layouts secundarios al principal
        layout_principal.addLayout(layout_encabezado)
        layout_principal.addLayout(layout_seleccion)
        layout_principal.addLayout(layout_datos)
        layout_principal.addLayout(layout_obtenerinfo)
        layout_principal.addLayout(layout_datoscompra)
        layout_principal.addLayout(layout_total)
        layout_principal.addLayout(layout_confirmacion)

        ############################## WIDGETS ##############################
        # Widgets del layout encabezado
        label_titulo = Caja("Compra de piezas", "Arial")
        label_ncompra = Caja("#{}".format(self.id_compra), "Arial")

        # Widgets del layout selección
        self.combobox_elemento = QComboBox()
        self.combobox_elemento.addItem("Oro")
        self.combobox_elemento.addItem("Plata")
        self.combobox_elemento.activated[str].connect(self.seleccion)

        self.checkbox_lote = QCheckBox("Por lote")
        self.checkbox_lote.stateChanged.connect(self.lote)

        self.combobox_pureza = QComboBox()
        self.combobox_pureza.setGeometry(0, 0, 100, 100)
        for dato in self.datos_oro:
            self.combobox_pureza.addItem(dato["Pureza"])
        self.combobox_pureza.activated[str].connect(self.seleccion_pureza)
        
        # Widgets del layout datos
        self.textbox_descripcion = QLineEdit()
        self.textbox_descripcion.setPlaceholderText("Descripción de la pieza")

        self.textbox_peso = QLineEdit()
        self.textbox_peso.setPlaceholderText("Peso de la pieza")

        # self.textbox_precio = QLineEdit()
        # self.textbox_precio.setPlaceholderText("Precio de la pieza")
        self.label_precio = Caja("Precio de la aleación")

        # Widgets del layout obtener info
        button_obtener = QPushButton("Calcular precio")
        button_obtener.clicked.connect(self.obtener_datos)

        # Widgets del layout datos compra
        self.table_compra = QTableWidget()
        # self.labels_encabezado = ["Descripcion", "Aleacion", "Peso", "Precio_calculado", "Precio_ingresado"]
        self.labels_encabezado = ["Descripcion", "Aleacion", "Peso_puro", "Precio"]
        self.table_compra.setColumnCount(len(self.labels_encabezado))
        self.table_compra.setHorizontalHeaderLabels(self.labels_encabezado)
        self.table_compra.itemChanged.connect(self.modificacion)

        # Widgets del layout total
        self.label_total = Caja("0", "Arial")

        # Widgets del layout confirmacion
        button_confirmar = QPushButton("Confirmar compra")
        button_confirmar.clicked.connect(self.confirmar)
                
        #######################################################################

        # Agregar los widgets al respectivo layout
        layout_encabezado.addWidget(Caja())
        layout_encabezado.addWidget(label_titulo)
        layout_encabezado.addWidget(label_ncompra)

        layout_seleccion.addWidget(self.combobox_elemento)
        layout_seleccion.addWidget(self.checkbox_lote)
        layout_seleccion.addWidget(self.combobox_pureza)
        
        layout_datos.addWidget(self.textbox_descripcion)
        layout_datos.addWidget(self.textbox_peso)
        # layout_datos.addWidget(self.textbox_precio)
        layout_datos.addWidget(self.label_precio)

        layout_obtenerinfo.addWidget(button_obtener)

        layout_datoscompra.addWidget(self.table_compra)

        layout_total.addWidget(Caja())
        layout_total.addWidget(Caja())
        layout_total.addWidget(self.label_total)

        layout_confirmacion.addWidget(button_confirmar)

        # Layout principal agregado a la ventana
        self.setLayout(layout_principal)

        # Atributo para cerrar todas las ventanas al cerrar la ventana principal
        self.setAttribute(Qt.WA_QuitOnClose, False)

    def seleccion(self, text):
        print(text)
        if text == "Plata":
            self.aleacion = "Ley 999"
            self.combobox_pureza.clear()
            for dato in self.datos_plata:
                self.combobox_pureza.addItem(dato["Pureza"])

            self.elemento = "Plata"
            self.precio = self.precio_plata

            self.porcentaje = self.datos_plata[0]["Porcentaje"]

        if text == "Oro":
            self.aleacion = "24K"
            self.combobox_pureza.clear()
            for dato in self.datos_oro:
                self.combobox_pureza.addItem(dato["Pureza"])

            self.elemento = "Oro"
            self.precio = self.precio_oro

            self.porcentaje = self.datos_oro[0]["Porcentaje"]

    def lote(self, state):
        if state == Qt.Checked:
            self.textbox_descripcion.setEnabled(False)
            self.descripcion_pieza = "Pieza de lote"
        if state == Qt.Unchecked:
            self.textbox_descripcion.setEnabled(True)
            self.descripcion_pieza = "No es una pieza de lote"

    def seleccion_pureza(self, text):
        print(text)
        self.aleacion = text
        
        if self.elemento == "Oro":
            for dato in self.datos_oro:
                if text == dato["Pureza"]:
                    self.precio = dato["Precio"]
                    self.porcentaje = dato["Porcentaje"]
        
        if self.elemento == "Plata":
            for dato in self.datos_plata:
                if text == dato["Pureza"]:
                    self.precio = dato["Precio"]
                    self.porcentaje = dato["Porcentaje"]

        print(self.precio)
        self.label_precio.setText("${} por gramo".format(self.precio))
  
    def obtener_datos(self):
        print("Datos obtenidos")

        self.total = 0

        if not self.descripcion_pieza == "Pieza de lote":
            self.descripcion_pieza = self.textbox_descripcion.text()
        
        self.peso_pieza = self.textbox_peso.text()
        
        # self.precio_ingresado = self.textbox_precio.text()

        if self.elemento == "Oro":
            
            # json_files.compra_oro(self.descripcion_pieza, self.peso_pieza, self.aleacion, self.porcentaje, self.precio_ingresado, self.precio)
            json_files.compra_oro(self.descripcion_pieza, self.peso_pieza, self.aleacion, self.porcentaje, self.precio)

            with open(json_compra_oro) as fichero_compra_oro:
                self.compras_oro = json.load(fichero_compra_oro)

            for compra in self.compras_oro:
                self.total = float(compra["Precio"]) + float(self.total)
                self.total = round(self.total, 2)
            
            self.table_compra.setRowCount(len(self.compras_oro))

            for i, fila in enumerate(self.compras_oro):
                for j, columna in enumerate(self.labels_encabezado):
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, fila[columna])
                    self.table_compra.setItem(i, j, item)
        else:
            # json_files.compra_plata(self.descripcion_pieza, self.peso_pieza, self.aleacion, self.porcentaje, self.precio_ingresado, self.precio)
            json_files.compra_plata(self.descripcion_pieza, self.peso_pieza, self.aleacion, self.porcentaje, self.precio)

            with open(json_compra_plata) as fichero_compra_plata:
                self.compras_plata = json.load(fichero_compra_plata)

            for compra in self.compras_plata:
                self.total = float(compra["Precio"]) + float(self.total)
                self.total = round(self.total, 2)
            
            self.table_compra.setRowCount(len(self.compras_plata))

            for i, fila in enumerate(self.compras_plata):
                for j, columna in enumerate(self.labels_encabezado):
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, fila[columna])
                    self.table_compra.setItem(i, j, item)
        
        self.label_total.setText("${}".format(self.total))
        self.nueva_compra = False

    def modificacion(self, item):
        if not self.nueva_compra:
            self.total = 0
            fila, campo = item.row(), self.labels_encabezado[item.column()]

            if self.elemento == "Oro":
                self.compras_oro[fila][campo] = item.data(Qt.EditRole)
                for compra in self.compras_oro:
                    self.total = float(compra["Precio"]) + float(self.total)
                    self.total = round(self.total, 2)

                with open(json_compra_oro, "w") as fichero_compra_oro:
                    json.dump(self.compras_oro, fichero_compra_oro)
            else:
                self.compras_plata[fila][campo] = item.data(Qt.EditRole)

                for compra in self.compras_plata:
                    self.total = float(compra["Precio"]) + float(self.total)
                    self.total = round(self.total, 2)

                with open(json_compra_plata, "w") as fichero_compra_plata:
                    json.dump(self.compras_plata, fichero_compra_plata)

        self.label_total.setText("${}".format(self.total))

    def confirmar(self):
        if self.elemento == "Oro":
            with open(json_compra_oro) as fichero_compra_oro:
                compras = json.load(fichero_compra_oro)
        
        if self.elemento == "Plata":
            with open(json_compra_plata) as fichero_compra_plata:
                compras = json.load(fichero_compra_plata)

        todas_las_compras = []
        piezas = []

        for compra in compras:
            compra_ind = []
            pieza_ind = []

            compra_ind.append(self.id_compra)
            compra_ind.append(compra["Precio"])
            compra_ind.append("0")
            # compra_ind.append(compra["Precio_ingresado"])

            pieza_ind.append(compra["Descripcion"])
            pieza_ind.append(compra["Peso_puro"])
            pieza_ind.append(compra["Aleacion"])
            pieza_ind.append(self.id_compra)

            todas_las_compras.append(compra_ind)
            piezas.append(pieza_ind)
        
        for c in todas_las_compras:
            db.actualizar_compra(c)

        for p in piezas:
            db.pieza(p)

        pdf.impresion_compra(self.id_compra, self.elemento, self.total)

        compra_realizada = QMessageBox.information(
                self, "Se creo la compra", "Se guardaron los datos de la compra en compras"
            )

class VentanaPrecios(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Actualización de precios")
        self.setMinimumSize(360, 700)

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(10)

        # Layouts secundarios
        layout_encabezado = QHBoxLayout()
        layout_seleccion = QHBoxLayout()
        layout_actualizar = QHBoxLayout()
        layout_infoprecios = QHBoxLayout()

        # Agregar layouts secundarios al principal
        layout_principal.addLayout(layout_encabezado)
        layout_principal.addLayout(layout_seleccion)
        layout_principal.addLayout(layout_actualizar)
        layout_principal.addLayout(layout_infoprecios)

        ############################## WIDGETS ##############################
        # Widgets del layout encabezado
        label_titulo = Caja("Actualizar precios", "Arial")

        # Widgets del layout selección
        self.list_seleccion = QComboBox()
        self.list_seleccion.addItem("Oro")
        self.list_seleccion.addItem("Plata")
        self.list_seleccion.activated[str].connect(self.seleccion)

        # Widgets del layout actualizar
        self.label_elemento = Caja("Oro 24K", "Arial")

        self.textbox_precio = QLineEdit()
        self.textbox_precio.setPlaceholderText("Precio")

        button_actualizar = QPushButton("Actualizar precios")
        button_actualizar.clicked.connect(self.actualizar)
        self.elemento = "Oro"

        # Widgets del layout infoprecios
        self.table_precios = QTableWidget()
        self.labels_encabezado = ["Pureza", "Porcentaje", "Precio"]
        self.table_precios.setColumnCount(len(self.labels_encabezado))
        self.table_precios.setHorizontalHeaderLabels(self.labels_encabezado)

        #####################################################################

        # Agregar widgets a los respectivos layouts
        layout_encabezado.addWidget(label_titulo)

        layout_seleccion.addWidget(self.list_seleccion)

        layout_actualizar.addWidget(self.label_elemento)
        layout_actualizar.addWidget(self.textbox_precio)
        layout_actualizar.addWidget(button_actualizar)

        layout_infoprecios.addWidget(self.table_precios)

        # Agregar layout principal a la ventana
        self.setLayout(layout_principal)
        
        # Atributo para cerrar todas las ventanas al cerrar la ventana principal
        self.setAttribute(Qt.WA_QuitOnClose, False)
    
    def seleccion(self, text):
        self.elemento = text

        if text == "Oro":
            self.label_elemento.setText("Oro 24K")
            
            if os.path.exists(json_oro):    
                with open(json_oro) as fichero_oro:
                    precios_oro = json.load(fichero_oro)
                
                self.table_precios.setRowCount(len(precios_oro))

                for i, fila in enumerate(precios_oro):
                    for j, columna in enumerate(self.labels_encabezado):
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, fila[columna])
                        self.table_precios.setItem(i, j, item)

        if text == "Plata":
            self.label_elemento.setText("Plata 999")

            if os.path.exists(json_plata):
                with open(json_plata) as fichero_plata:
                    precios_plata = json.load(fichero_plata)
                
                self.table_precios.setRowCount(len(precios_plata))

                for i, fila in enumerate(precios_plata):
                    for j, columna in enumerate(self.labels_encabezado):
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, fila[columna])
                        self.table_precios.setItem(i, j, item)

    def actualizar(self):
        print(self.elemento)
        print(self.textbox_precio.text())

        if self.elemento == "Oro":
            json_files.precios_oro(float(self.textbox_precio.text()))

            with open(json_oro) as fichero_oro:
                precios_oro = json.load(fichero_oro)
            
            self.table_precios.setRowCount(len(precios_oro))

            for i, fila in enumerate(precios_oro):
                for j, columna in enumerate(self.labels_encabezado):
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, fila[columna])
                    self.table_precios.setItem(i, j, item)
        
            db.actualizar_precio_oro(float(self.textbox_precio.text()))

        if self.elemento == "Plata":
            json_files.precios_plata(float(self.textbox_precio.text()))

            with open(json_plata) as fichero_plata:
                precios_plata = json.load(fichero_plata)
            
            self.table_precios.setRowCount(len(precios_plata))

            for i, fila in enumerate(precios_plata):
                for j, columna in enumerate(self.labels_encabezado):
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, fila[columna])
                    self.table_precios.setItem(i, j, item)

            db.actualizar_precio_plata(float(self.textbox_precio.text()))
    
        self.textbox_precio.clear()

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        # Actualización de la base de datos
        db.database_exists()

        # Configuración de la ventana
        self.setWindowTitle("RAISA APP")
        self.setMinimumSize(QSize(600, 300))
        # self.showMaximized()

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(10)

        # Layouts secundarios
        layout_encabezado = QHBoxLayout()
        layout_actualizacion = QHBoxLayout()
        layout_acciones = QHBoxLayout()
        layout_consultas = QHBoxLayout()

        # Agregar layouts secundarios al principal
        layout_principal.addLayout(layout_encabezado)
        layout_principal.addLayout(layout_actualizacion)
        layout_principal.addLayout(layout_acciones)
        layout_principal.addLayout(layout_consultas)

        ############################## WIDGETS ##############################
        # Widgets del layout encabezado
        label_logo = Caja()
        logo = QPixmap(r"C:\raisa-bruker\images\logo.png")
        label_logo.setPixmap(logo)
        label_logo.setScaledContents(False)

        label_titulo = Caja("SUSY JOYAS", "Arial")

        fechahoy = formats.format_fecha_hoy(datetime.today())
        label_fechahoy = Caja(fechahoy, "Arial")

        # Widgets del layout actualización
        button_actualizar = QPushButton("Actualizar precios")
        button_actualizar.clicked.connect(self.actualizar_precios)

        # Widgets del layout acciones
        button_compras = QPushButton("Compra de piezas")
        button_compras.clicked.connect(self.comprar_piezas)

        button_ventas = QPushButton("Venta de analisis")
        button_ventas.clicked.connect(self.venta_analisis)

        # Widgets del layout consultas
        button_consultas = QPushButton("Consultas de ventas")
        button_consultas.clicked.connect(self.consultas)

        #####################################################################

        # Agregar widgets a los respectivos layouts
        layout_encabezado.addWidget(label_logo)
        layout_encabezado.addWidget(label_titulo)
        layout_encabezado.addWidget(label_fechahoy)

        layout_actualizacion.addWidget(Caja())
        layout_actualizacion.addWidget(button_actualizar)
        layout_actualizacion.addWidget(Caja())

        layout_acciones.addWidget(button_compras)
        layout_acciones.addWidget(button_ventas)

        layout_consultas.addWidget(button_consultas)

        # Layout principal agregado a la ventana
        widget = QWidget()
        widget.setLayout(layout_principal)
        self.setCentralWidget(widget)

    def actualizar_precios(self):
        print("Actualizar precios")

        self.window_precios = VentanaPrecios()
        self.window_precios.show()
    
    def comprar_piezas(self):
        print("Comprar piezas")

        if len(db.ultimo_precio_oro()) == 0 or len(db.ultimo_precio_plata()) == 0 or not os.path.exists(json_oro) or not os.path.exists(json_plata):
            faltan_precios = QMessageBox.critical(
                self, "Faltan precios", "Se abrirá la ventana de actualización"
            )

            self.window_precios = VentanaPrecios()
            self.window_precios.show()
        else:
            self.window_compras = VentanaCompras()
            self.window_compras.show()

    def venta_analisis(self):
        print("Vender analisis")

        self.window_venta = VentanaVentas()
        self.window_venta.show()

    def consultas(self):
        print("Consulta de ventas")

        self.window_consulta = VentanaConsultas()
        self.window_consulta.show()

if __name__=="__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = VentanaPrincipal()

    window.show()
    sys.exit(app.exec())

