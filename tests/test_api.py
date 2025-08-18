import json
import sys
from pathlib import Path
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"
    assert "version" in data

def test_predict_validation_error():
    r = client.post("/predict", json={})
    assert r.status_code == 422

def test_predict_with_dummy_base64(monkeypatch):
    # Crear una imagen pequeña en memoria
    from PIL import Image
    import base64, io
    img = Image.new("RGB", (50, 50), color=(120, 30, 200))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    # Forzar modelo dummy para rapidez
    from app.main import model_service
    model_service.model = "dummy"  # type: ignore

    r = client.post("/predict", json={"image_base64": b64})
    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data
    assert "probabilities" in data
    assert "metadata" in data
