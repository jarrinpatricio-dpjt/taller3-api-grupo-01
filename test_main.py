"""
test_main.py - Pruebas automatizadas con pytest.

Ejecutar:   pytest -v
GitHub Actions las ejecuta automáticamente en cada push.
"""

from fastapi.testclient import TestClient

from main import app

cliente = TestClient(app)


def obtener_token(usuario="ana", password="ana123"):
    respuesta = cliente.post("/api/v1/token",
                             data={"username": usuario, "password": password})
    return respuesta.json()["access_token"]


def encabezado(token):
    return {"Authorization": f"Bearer {token}"}


# ---------------- Pruebas mínimas exigidas por el taller ------------------
def test_sin_token_es_rechazado():
    respuesta = cliente.get("/api/v1/solicitudes")
    assert respuesta.status_code == 401


def test_con_token_valido_es_aceptado():
    respuesta = cliente.get("/api/v1/solicitudes", headers=encabezado(obtener_token()))
    assert respuesta.status_code == 200
    assert len(respuesta.json()) >= 1


def test_solicitud_inexistente_devuelve_404():
    respuesta = cliente.get("/api/v1/solicitudes/9999", headers=encabezado(obtener_token()))
    assert respuesta.status_code == 404


# ------------------------ Pruebas adicionales -----------------------------
def test_password_incorrecta_devuelve_401():
    respuesta = cliente.post("/api/v1/token",
                             data={"username": "ana", "password": "equivocada"})
    assert respuesta.status_code == 401


def test_token_alterado_es_rechazado():
    token = obtener_token() + "x"
    respuesta = cliente.get("/api/v1/solicitudes", headers=encabezado(token))
    assert respuesta.status_code == 401


def test_no_puede_ver_solicitud_de_otro_usuario():
    # El solicitud 3 pertenece a "luis"; "ana" no debe verlo.
    respuesta = cliente.get("/api/v1/solicitudes/3", headers=encabezado(obtener_token()))
    assert respuesta.status_code == 404


def test_registrar_solicitud_devuelve_201():
    respuesta = cliente.post("/api/v1/solicitudes", json={"tipo": "Consulta de gastroenterología"},
                             headers=encabezado(obtener_token()))
    assert respuesta.status_code == 201
    assert respuesta.json()["estado"] == "Recibido"
