# Producto-Datos-ML-API

Despliegue de un modelo de Machine Learning como API con FastAPI.

## Requisitos

- Python 3.10 o 3.11
- Windows PowerShell (este README incluye comandos para PowerShell)

## Instalación (local)

1. Crear entorno virtual (opcional):

    ```powershell
    python -m venv .venv; .\.venv\Scripts\Activate.ps1
    ```

1. Instalar dependencias:

    ```powershell
    python -m pip install --upgrade pip; python -m pip install -r requirements.txt
    ```

1. Ejecutar servidor local:

    ```powershell
    python -c "import uvicorn, os; os.chdir('c:/Users/Cesar/Producto-Datos-ML-API'); uvicorn.run('app.main:app', host='127.0.0.1', port=8000)"
    ```

1. Probar endpoints:

    - Navega a <http://127.0.0.1:8000/docs> para Swagger UI.
    - Cliente de ejemplo:

    ```powershell
    python client/client.py
    ```

## Contrato de API (resumen)

- GET /health → `{ status: "ok", version: "0.1.0" }`
- POST /predict (JSON):
  - Uno de: `image_url` (URL pública) o `image_base64` (cadena base64)
  - Respuesta: `prediction`, `probabilities`, `metadata` (incluye `ndvi`, `ndwi`)

Ver `docs/API_CONTRACT.md` para detalles completos.

## Ejemplos Rápidos

Petición con URL (PowerShell):
```powershell
$body = @{ image_url = "https://picsum.photos/200/300" } | ConvertTo-Json
Invoke-RestMethod -Uri https://producto-datos-ml-api.onrender.com/predict -Method Post -Body $body -ContentType 'application/json'
```

Petición con Base64 (ejemplo ficticio):
```powershell
$b64 = Get-Content .\tests\sample.b64 -Raw
$body = @{ image_base64 = $b64 } | ConvertTo-Json
Invoke-RestMethod -Uri https://producto-datos-ml-api.onrender.com/predict -Method Post -Body $body -ContentType 'application/json'
```

## Checklist QA Local

- [ ] `uvicorn app.main:app` levanta sin errores
- [ ] GET /health → 200 y contiene `status` y `version`
- [ ] POST /predict con `image_url` válida → 200 y `prediction`
- [ ] POST /predict con `image_base64` válida → 200
- [ ] POST /predict sin campos → 422
- [ ] Probabilities suman ≈ 1
- [ ] `models/xception_satellite.h5` y `models/labels.json` presentes

## URL Despliegue (Render)

🚀 **API en vivo:** https://producto-datos-ml-api.onrender.com

- **Health Check:** https://producto-datos-ml-api.onrender.com/health
- **Documentación:** https://producto-datos-ml-api.onrender.com/docs
- **API Endpoint:** https://producto-datos-ml-api.onrender.com/predict

✅ **Estado:** Desplegado y funcionando correctamente

## Exportar modelo desde el Notebook

Al final del notebook `notebooks/Tarea_4A_Computer_Vision_satellite-images-classification.ipynb` se agregó una celda para exportar:

- `models/xception_satellite.h5`
- `models/labels.json` con `class_names` e `img_size`

Ejecuta el notebook hasta el final y verifica que ambos archivos existan en `models/`.

## Despliegue en Render (resumen)

- Crea un servicio Web (Python) en Render.
- Define el comando de inicio:

    ```powershell
    uvicorn app.main:app --host 0.0.0.0 --port $PORT
    ```

- Asegúrate de subir `requirements.txt` y (opcionalmente) considera `tensorflow-cpu` si usarás el modelo Keras en Render.
- Actualiza este README con la URL pública cuando esté lista.

## Modelo de ML (archivo grande excluido)

El archivo original `models/xception_satellite.h5` supera el límite de 100MB de GitHub y se excluyó en `.gitignore`.

Para usar un modelo real coloca uno de los siguientes en `models/` (ignorados por git):

1. `xception_satellite.tflite` (recomendado, versión convertida y optimizada)
2. `xception_satellite.h5` (si lo tienes localmente)

Conversión a TFLite (reduce tamaño):

```powershell
python scripts/convert_to_tflite.py
```

Carga preferente: la app intenta primero `xception_satellite.tflite`, luego `.h5`; si no existe ninguno usa un modelo dummy.
