import os
import sys
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from datetime import datetime

import db, formats, json_files

# Rutas generales
json_oro = r"C:\raisa-bruker\files\precios_oro.json"
json_plata = r"C:\raisa-bruker\files\precios_plata.json"

json_compra_oro = r"C:\raisa-bruker\files\compra_oro.json"
json_compra_plata = r"C:\raisa-bruker\files\compra_plata.json"

class Caja(QLabel):
    def __init__(self, texto="", fuente="Arial", tam=16, color="", alV=Qt.AlignVCenter, alH=Qt.AlignHCenter):
        super().__init__()

        self.setStyleSheet(f"background-color:{color}")
        self.setText(texto)
        font = QFont(fuente, tam)
        self.setFont(font)
        self.setAlignment(alH | alV)

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

        # Variable porcentaje
        self.porcentaje = 0

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

        self.textbox_precio = QLineEdit()
        self.textbox_precio.setPlaceholderText("Precio de la pieza")

        # Widgets del layout obtener info
        button_obtener = QPushButton("Calcular precio")
        button_obtener.clicked.connect(self.obtener_datos)

        # Widgets del layout datos compra
        self.table_compra = QTableWidget()
        self.labels_encabezado = ["Descripcion", "Aleacion", "Peso", "Precio_calculado", "Precio_ingresado"]
        self.table_compra.setColumnCount(len(self.labels_encabezado))
        self.table_compra.setHorizontalHeaderLabels(self.labels_encabezado)

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
        layout_datos.addWidget(self.textbox_precio)

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
        
        if text == "Oro":
            self.aleacion = "24K"
            self.combobox_pureza.clear()
            for dato in self.datos_oro:
                self.combobox_pureza.addItem(dato["Pureza"])

            self.elemento = "Oro"
            self.precio = self.precio_oro

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
        
    def obtener_datos(self):
        print("Datos obtenidos")

        self.total = 0

        if not self.descripcion_pieza == "Pieza de lote":
            self.descripcion_pieza = self.textbox_descripcion.text()
        
        self.peso_pieza = self.textbox_peso.text()
        
        self.precio_ingresado = self.textbox_precio.text()

        if self.elemento == "Oro":
            
            json_files.compra_oro(self.descripcion_pieza, self.peso_pieza, self.aleacion, self.porcentaje, self.precio_ingresado, self.precio)

            with open(json_compra_oro) as fichero_compra_oro:
                compras_oro = json.load(fichero_compra_oro)

            for compra in compras_oro:
                self.total = float(compra["Precio_ingresado"]) + float(self.total)
                self.total = round(self.total, 2)
            
            self.table_compra.setRowCount(len(compras_oro))

            for i, fila in enumerate(compras_oro):
                for j, columna in enumerate(self.labels_encabezado):
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, fila[columna])
                    self.table_compra.setItem(i, j, item)
        else:
            json_files.compra_plata(self.descripcion_pieza, self.peso_pieza, self.aleacion, self.porcentaje, self.precio_ingresado, self.precio)

            with open(json_compra_plata) as fichero_compra_plata:
                compras_plata = json.load(fichero_compra_plata)

            for compra in compras_plata:
                self.total = float(compra["Precio_ingresado"]) + float(self.total)
                self.total = round(self.total, 2)
            
            self.table_compra.setRowCount(len(compras_plata))

            for i, fila in enumerate(compras_plata):
                for j, columna in enumerate(self.labels_encabezado):
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, fila[columna])
                    self.table_compra.setItem(i, j, item)
        
        self.label_total.setText(str(self.total))

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
            compra_ind.append(compra["Precio_calculado"])
            compra_ind.append(compra["Precio_ingresado"])

            pieza_ind.append(compra["Descripcion"])
            pieza_ind.append(compra["Peso"])
            pieza_ind.append(compra["Aleacion"])
            pieza_ind.append(self.id_compra)

            todas_las_compras.append(compra_ind)
            piezas.append(pieza_ind)
        
        for c in todas_las_compras:
            db.actualizar_compra(c)

        for p in piezas:
            db.pieza(p)


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

        # Agregar layouts secundarios al principal
        layout_principal.addLayout(layout_encabezado)
        layout_principal.addLayout(layout_actualizacion)
        layout_principal.addLayout(layout_acciones)

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








if __name__=="__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = VentanaPrincipal()

    window.show()
    sys.exit(app.exec())

