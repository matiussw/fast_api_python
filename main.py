from fastapi import FastAPI
from routers import productos 
from database import db

app = FastAPI(
    title="API de la Tienda",
    description="CRUD de productos y categorias organizado en varios archivos",
    version="2.0.0",
)

conexion =db.crearTablas()

app.include_router(productos.router)


@app.get("/" ,tags=["Inicio"] )
def inicio():
    return{"Mensaje":"Api Tienda"}

