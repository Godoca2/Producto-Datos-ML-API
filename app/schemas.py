from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict, Any


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str


class PredictRequest(BaseModel):
    # Dos opciones de entrada: URL o base64. Al menos una requerida.
    image_url: Optional[HttpUrl] = Field(
        default=None, description="URL pública de la imagen a clasificar"
    )
    image_base64: Optional[str] = Field(
        default=None, description="Imagen en base64 (data sin prefijo)"
    )


class PredictResponse(BaseModel):
    prediction: str
    probabilities: Optional[Dict[str, float]] = None
    metadata: Optional[Dict[str, Any]] = None
