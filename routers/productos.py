from fastapi import APIRouter, HTTPException
from modelos import modelos
from database import db

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("")
def ListarProductos():
    conexion = db.obtener_conexion()
    filas = conexion.execute("SELECT * FROM productos").fetchall()
    conexion.close()
    return [dict(fila) for fila in filas]


@router.post("", status_code=201)
def IngresarProductos(datos: modelos.ProductosEntrada):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO productos (nombre, precio, categoria) VALUES (?, ?, ?)",
        (datos.nombre, datos.precio, datos.categoria),
    )

    id = cursor.lastrowid      # el id lo asigna SQLite, ya no se calcula a mano
    conexion.commit()          # sin commit, el INSERT no queda guardado
    conexion.close()

    return {"Producto Creado": {"id": id, **datos.model_dump()}}


@router.put("/{id_producto}")
def ActualizarProductos(id_producto: int, datos: modelos.ProductosEntrada):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "UPDATE productos SET nombre = ?, precio = ?, categoria = ? WHERE id = ?",
        (datos.nombre, datos.precio, datos.categoria, id_producto),
    )

    # rowcount dice cuántas filas cambiaron; 0 = ese id no existía
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    conexion.commit()
    conexion.close()

    return {"Producto actualizado": {"id": id_producto, **datos.model_dump()}}


@router.delete("/{id_producto}")
def EliminarProductos(id_producto: int):
    conexion = db.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))

    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    conexion.commit()
    conexion.close()

    return {"Producto Eliminado": id_producto}