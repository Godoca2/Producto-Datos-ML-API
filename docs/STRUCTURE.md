# Estructura del Proyecto

- `app/`: Código de la API (FastAPI) y routers.
- `client/`: Scripts o notebooks de cliente para probar la API.
- `configs/`: Archivos de configuración (e.g., rutas de modelo). No subir secretos.
- `data/`: Datos (raw, interim, processed, external). Ignorados por git salvo .gitkeep.
- `docs/`: Documentación adicional (contratos, arquitectura, etc.).
- `models/`: Artefactos del modelo serializado (.pkl/.joblib). Ignorados por git salvo .gitkeep.
- `notebooks/`: Exploración y prototipos.
- `scripts/`: Utilidades (e.g., exportar requirements).
- `src/producto_datos_ml_api/`: Código reutilizable de la librería/paquete Python.
- `tests/`: Pruebas automatizadas.

Siguientes pasos:

1. Añadir FastAPI y endpoints en `app/`.
2. Colocar el modelo en `models/` y la lógica de carga en `src/` o `app/`.
3. Crear `client/client.py` con ≥3 requests a la API.
4. Completar README con instalación, ejecución local y payloads.
