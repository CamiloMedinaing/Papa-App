from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Lista donde se guardan los agricultores
agricultores = []

# Modelo del agricultor
class Agricultor(BaseModel):
    id: int
    cedula: str
    nombre: str
    area: float
    cultivo: str
    inversion: float
    fecha: str
    ubicacion_cultivo: str

# Ruta principal
@app.get("/")
def inicio():
    return {
        "mensaje": "Servidor funcionando",
        "cantidad_agricultores": len(agricultores)
    }

# Registrar agricultor
@app.post("/crear_agricultor")
def crear_agricultor(agricultor: Agricultor):

    agricultores.append(agricultor.dict())

    return {
        "mensaje": "Agricultor registrado correctamente",
        "datos": agricultor
    }

# Mostrar agricultores
@app.get("/agricultores")
def mostrar_agricultores():
    return agricultores