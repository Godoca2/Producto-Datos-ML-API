"""
Cliente de ejemplo.
Reemplaza la URL y el payload cuando la API esté lista.
"""

import base64
from pathlib import Path

import requests

BASE_URL = "http://127.0.0.1:8000"  # reemplazar por URL de Render al desplegar


def test_health():
    r = requests.get(f"{BASE_URL}/health", timeout=10)
    print("/health:", r.status_code, r.json())


def test_predict_url():
    payload = {
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST-SM4.jpeg/320px-HST-SM4.jpeg"
    }
    r = requests.post(f"{BASE_URL}/predict", json=payload, timeout=20)
    print("/predict (url):", r.status_code, r.json())


def test_predict_base64():
    # Usa una imagen pequeña local si existe
    sample = Path("tests/sample.jpg")
    if not sample.exists():
        print("No hay tests/sample.jpg; omitiendo base64 test")
        return
    b64 = base64.b64encode(sample.read_bytes()).decode("utf-8")
    payload = {"image_base64": b64}
    r = requests.post(f"{BASE_URL}/predict", json=payload, timeout=20)
    print("/predict (base64):", r.status_code, r.json())


if __name__ == "__main__":
    test_health()
    test_predict_url()
    test_predict_base64()
