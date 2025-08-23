from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import requests

from .schemas import HealthResponse, PredictRequest, PredictResponse
from .model_service import ModelService, load_image_from_base64
from .indices import calcular_indices

APP_VERSION = "0.1.0"


from fastapi.responses import HTMLResponse

app = FastAPI(title="Producto-Datos-ML-API", version=APP_VERSION)
model_service = ModelService(class_names=["urban", "rural"])  # ajusta a tus clases
model_service.load()

# Endpoint profesional en la raíz
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head><title>Producto-Datos-ML-API</title></head>
        <body style='font-family:sans-serif;'>
            <h1>🚀 API de Clasificación de Imágenes Satelitales</h1>
            <p>Bienvenido. Esta API está activa y lista para pruebas profesionales.</p>
            <ul>
                <li><a href='/docs'>Documentación interactiva (Swagger UI)</a></li>
                <li><a href='/health'>Health check</a></li>
                <li><b>POST /predict</b>: Endpoint para predicción (ver /docs)</li>
            </ul>
            <p>Para pruebas automáticas, consulta el README del repositorio.</p>
        </body>
    </html>
    """


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(version=APP_VERSION)


@app.post("/predict", response_model=PredictResponse)
async def predict(payload: PredictRequest):
    if not payload.image_url and not payload.image_base64:
        raise HTTPException(status_code=422, detail="Debes enviar image_url o image_base64")

    try:
        if payload.image_url:
            resp = requests.get(str(payload.image_url), timeout=10)
            resp.raise_for_status()
            from PIL import Image
            import io

            image = Image.open(io.BytesIO(resp.content))
        else:
            image = load_image_from_base64(payload.image_base64)  # type: ignore[arg-type]

        result = model_service.predict(image)
        ndvi, ndwi = calcular_indices(image)
        return PredictResponse(
            prediction=result["prediction"],
            probabilities=result.get("probabilities"),
            metadata={"model_version": APP_VERSION, "ndvi": ndvi, "ndwi": ndwi},
        )
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except requests.RequestException as re:
        raise HTTPException(status_code=400, detail=f"Error al descargar imagen: {re}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")
