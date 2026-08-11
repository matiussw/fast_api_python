import sqlite3 

DB_NAME="Store.db"

def obtener_conexion():
    conexion=sqlite3.connect(DB_NAME,check_same_thread=False)
    conexion.row_factory=sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion

def crearTablas():
    conexion=obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        Nombre TEXT NOT NULL UNIQUE
        )
        """
        )

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    Nombre TEXT NOT NULL UNIQUE, 
    Precio FLOAT,
    Id_categoria INTEGER ,
    FOREIGN KEY (Id_categoria) REFERENCES Categoria (id)
    )
    """
    )
   

    conexion.commit()
    conexion.close()
    print(f"[BD] Tablas verificadas en {DB_NAME}")
