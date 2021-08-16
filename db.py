import os

import sqlite3
from sqlite3 import Error

from datetime import datetime

db_file = r"C:\raisa-bruker\database\susyjoyas.db"

# Tablas de Susy Joyas
tablas = [
    """CREATE TABLE precio_oro(
        id_oro INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        actualizacion DATETIME NOT NULL,
        oro24K REAL NOT NULL
    )   
    """,
    """CREATE TABLE precio_plata(
        id_plata INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        actualizacion DATETIME NOT NULL,
        plata999 REAL NOT NULL
    )
    """,
    """CREATE TABLE compra(
        id_compra INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        fecha_compra DATE NOT NULL,
        precio_calculado REAL NOT NULL,
        precio_compra REAL NOT NULL,
        id_oro INTEGER NOT NULL REFERENCES precio_oro(id_oro) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
        id_plata INTEGER NOT NULL REFERENCES precio_oro(id_plata) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
    )
    """,
    """CREATE TABLE pieza(
        id_pieza INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(150) NOT NULL,
        peso REAL NOT NULL,
        aleacion VARCHAR(150) NOT NULL,
        id_compra INTEGER NOT NULL REFERENCES compra(id_compra) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
    )
  """
]

def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, sql_table):
    try:
        c = conn.cursor()
        c.execute(sql_table)
    except Error as e:
        print(e)

def create_db(tablas):
    for t in tablas:
        print(t)
        create_table(create_connection(db_file), t)

def database_exists():
    if not os.path.exists(db_file):
        create_db(tablas)

def actualizar_precio_oro(precio):
    conn = create_connection(db_file)
    db = conn.cursor()

    momento_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    update = (momento_actualizacion, precio)

    db.execute(
        """
            INSERT INTO precio_oro(
                actualizacion, oro24K
            )
            VALUES (?, ?)
        """, update
    )

    conn.commit()
    print("Precio del oro actualizado")

def ultimo_precio_oro():
    conn = create_connection(db_file)
    db = conn.cursor()

    db.execute(
        """
            SELECT *
            FROM precio_oro
            ORDER BY id_oro
            DESC LIMIT 1;
        """
    )

    ultimo_precio = db.fetchall()
    
    return ultimo_precio

def actualizar_precio_plata(precio):
    conn = create_connection(db_file)
    db = conn.cursor()

    momento_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    update = (momento_actualizacion, precio)

    db.execute(
        """
            INSERT INTO precio_plata(
                actualizacion, plata999
            )
            VALUES (?, ?)
        """, update
    )

    conn.commit()
    print("Precio de la plata actualizado")

def ultimo_precio_plata():
    conn = create_connection(db_file)
    db = conn.cursor()

    db.execute(
        """
            SELECT *
            FROM precio_plata
            ORDER BY id_plata
            DESC LIMIT 1;
        """
    )

    ultimo_precio = db.fetchall()

    return ultimo_precio

def crear_compra(datos_compra):
    conn = create_connection(db_file)
    db = conn.cursor()

    fecha_compra = datetime.now().strftime("%Y-%m-%d")

    datos_compra.insert(0, fecha_compra)
    
    db.execute(
        """
            INSERT INTO compra(
                fecha_compra, precio_calculado, precio_compra, id_oro, id_plata
            )
            VALUES(?, ?, ?, ?, ?)
        """, tuple(datos_compra)
    )

    conn.commit()
    print("Compra actualizada")

def ultima_compra():
    conn = create_connection(db_file)
    db = conn.cursor()

    db.execute(
        """
            SELECT *
            FROM compra
            ORDER BY id_compra
            DESC LIMIT 1;
        """
    )

    ultima_compra = db.fetchall()

    return ultima_compra

def actualizar_compra(nuevos_datos):
    conn = create_connection(db_file)
    db = conn.cursor()

    id_compra, precio_calculado, precio_ingresado = tuple(nuevos_datos)
    db.execute(
        """
            UPDATE compra
            SET precio_calculado = {}, precio_compra={}
            WHERE id_compra = {}
        """.format(precio_calculado, precio_ingresado, id_compra)
    )

    conn.commit()

    print("Compra actualizada")

def pieza(datos):
    conn = create_connection(db_file)
    db = conn.cursor()

    db.execute(
        """
            INSERT INTO pieza(
                nombre, peso, aleacion, id_compra
            )
            VALUES(?, ?, ?, ?)
        """, tuple(datos)
    )

    conn.commit()
    print("Pieza creada")

