"""
main.py - API REST de Solicitudes de Citas (código base del Taller 3).

Ejecutar:                                     uvicorn main:app --reload
Documentación interactiva (Swagger UI):       http://localhost:8000/docs
Contrato OpenAPI:                             http://localhost:8000/openapi.json
"""

from datetime import date

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

import datos
from seguridad import autenticar_usuario, crear_token, obtener_usuario_actual

app = FastAPI(
    title="API de Solicitudes de Citas",
    version="1.0.0",
    description="API que expone de forma segura el servicio de solicitudes de citas de gastroenterología "
                "de un sistema heredado. Taller 3 - Gestión de Servicios en la Nube.",
)


# ------------------------- Modelos (esquemas) -----------------------------
# Definen qué datos entran y salen. FastAPI los usa para validar y para
# generar el contrato OpenAPI automáticamente.
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SolicitudNueva(BaseModel):
    tipo: str = Field(..., min_length=3, max_length=100,
                      examples=["Consulta de gastroenterología"])


class Solicitud(BaseModel):
    id: int
    tipo: str
    estado: str
    fecha: date
    # Nota: el campo "propietario" NO se expone; es un dato interno.


# ------------------------------ Endpoints ---------------------------------
@app.get("/", tags=["Estado"])
def estado_servicio():
    """Verifica que la API está en línea (health check)."""
    return {"servicio": "API de Solicitudes de Citas", "estado": "en línea"}


@app.post("/api/v1/token", response_model=Token, tags=["Autenticación"])
def obtener_token(formulario: OAuth2PasswordRequestForm = Depends()):
    """Recibe usuario y contraseña y devuelve un token JWT."""
    usuario = autenticar_usuario(formulario.username, formulario.password)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=crear_token(usuario["usuario"]))


@app.get("/api/v1/solicitudes", response_model=list[Solicitud], tags=["Solicitudes de Citas"])
def listar_solicitudes(usuario=Depends(obtener_usuario_actual)):
    """Lista las solicitudes del usuario autenticado."""
    return datos.listar_solicitudes(usuario["usuario"])


@app.get("/api/v1/solicitudes/{solicitud_id}", response_model=Solicitud, tags=["Solicitudes de Citas"],
         responses={404: {"description": "Solicitud no encontrada"}})
def consultar_solicitud(solicitud_id: int, usuario=Depends(obtener_usuario_actual)):
    """Consulta el estado de una solicitud del usuario autenticado."""
    solicitud = datos.buscar_solicitud(solicitud_id)
    # Si la solicitud no existe o pertenece a otra persona se responde 404,
    # para no revelar información de otros usuarios.
    if solicitud is None or solicitud["propietario"] != usuario["usuario"]:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud


@app.post("/api/v1/solicitudes", response_model=Solicitud,
          status_code=status.HTTP_201_CREATED, tags=["Solicitudes de Citas"])
def registrar_solicitud(nuevo: SolicitudNueva, usuario=Depends(obtener_usuario_actual)):
    """Registra un nuevo solicitud a nombre del usuario autenticado."""
    return datos.registrar_solicitud(nuevo.tipo, usuario["usuario"])
