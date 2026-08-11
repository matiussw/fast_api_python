from pydantic import BaseModel

class ProductosEntrada(BaseModel):
    nombre: str
    precio: float
    categoria : str 


