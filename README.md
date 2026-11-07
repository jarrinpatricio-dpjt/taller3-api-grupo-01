# API de Solicitudes de Citas de Gastroenterología

Adaptación del código base del docente para el Taller 3 de UBE.
Alcance: registrar y consultar solicitudes propias. No agenda horarios ni confirma citas.
Los datos ficticios están en memoria y se reinician al reiniciar el proceso.
La fecha corresponde al registro, no a la atención. No usar datos reales.

## Ejecutar en Windows desde CMD

Abrir esta carpeta (donde está main.py) y ejecutar:

```bat
py -3.12 -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Requiere Python 3.11 o superior; si se usa otra versión instalada, adaptar el primer comando.
Swagger: http://localhost:8000/docs
Contrato: http://localhost:8000/openapi.json
Usuarios ficticios: ana / ana123 y luis / luis123.
La clave JWT predeterminada es solo de demostración; JWT_SECRET permite reemplazarla.

## Evidencias de Swagger

1. Sin pulsar Authorize, ejecutar GET /api/v1/solicitudes: 401.
2. Pulsar Authorize e ingresar ana y ana123; ejecutar el mismo GET: 200.
3. Ejecutar GET /api/v1/solicitudes/9999 autenticado: 404.
4. Ejecutar POST /api/v1/solicitudes con {"tipo":"Consulta de gastroenterología"}: 201.
5. Guardar capturas y descargar openapi.json si se modifica el código.

## Pruebas

En otra terminal, activar el entorno y ejecutar `python -m pytest -v`.
Se conservan las siete pruebas del profesor, adaptadas al caso.

## GitHub Actions

Subir el contenido de esta carpeta a la raíz del repositorio, incluida .github/workflows/ci.yml.
No subir venv, .env ni carpetas de caché. El pipeline se ejecuta con push y pull_request.
Para la evidencia roja, cambiar temporalmente en main.py el código de respuesta de solicitud
no encontrada de 404 a 400. Subir el cambio y capturar las pruebas fallidas en Actions.
Restaurar 404, subir la corrección y capturar la ejecución verde. No dejar el fallo en la versión final.
El pipeline ejecuta pruebas; no despliega ni bloquea por sí solo una publicación.

## Estado de la entrega

Pruebas locales verificadas: siete aprobadas. openapi.json generado desde la aplicación.
Pendientes: repositorio del grupo, evidencias reales de Swagger y Actions y datos de portada.
Las versiones mínimas de requirements.txt se mantienen como en el material del docente.
