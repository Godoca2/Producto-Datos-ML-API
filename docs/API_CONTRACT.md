# Contrato de la API

Versión de la aplicación: `0.1.0`

## 1. Endpoints

### GET /health

Devuelve el estado básico del servicio.

Ejemplo de respuesta:

```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

### POST /predict

Clasifica una imagen satelital usando el modelo exportado (Xception fine-tuned u otro seleccionado) y calcula índices NDVI/NDWI aproximados.

Headers:

- `Content-Type: application/json`

Cuerpo (una de las dos variantes, debes enviar **exactamente uno** de los campos `image_url` o `image_base64`):

Ejemplo usando URL:

```json
{
  "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST-SM4.jpeg/320px-HST-SM4.jpeg"
}
```

Ejemplo usando Base64 (solo el string, sin prefijo `data:`):

```json
{
  "image_base64": "/9j/4AAQSkZJRgABAQAAAQABAAD..."
}
```

Ejemplo de respuesta exitosa:

```json
{
  "prediction": "7",
  "probabilities": {
    "0": 0.12,
    "1": 0.03,
    "2": 0.04,
    "3": 0.05,
    "4": 0.02,
    "5": 0.01,
    "6": 0.08,
    "7": 0.42,
    "8": 0.07,
    "9": 0.05,
    "10": 0.04,
    "11": 0.02,
    "12": 0.03,
    "13": 0.02
  },
  "metadata": {
    "model_version": "0.1.0",
    "ndvi": 0.0012,
    "ndwi": -0.0134
  }
}
```

Campos de la respuesta:

- `prediction`: Nombre (string) de la clase con mayor probabilidad.
- `probabilities`: Mapa clase → probabilidad (float) normalizada a 1.
- `metadata`: Información adicional:
  - `model_version`: versión de la app / modelo.
  - `ndvi`, `ndwi`: índices calculados de forma **aproximada** (proxy RGB, no usar como valor espectral oficial).

## 2. Validaciones y Errores

| Código | Causa | Ejemplo de `detail` |
|--------|-------|----------------------|
| 422 | Ninguno de `image_url` / `image_base64` presente | "Debes enviar image_url o image_base64" |
| 400 | URL inaccesible / error de descarga | "Error al descargar imagen" |
| 500 | Error interno no controlado | "Error interno" |

Si se envían ambos campos (`image_url` y `image_base64`) actualmente se procesa `image_url`; se recomienda enviar solo uno.

## 3. Modelo

- Archivo: `models/xception_satellite.h5`
- Metadatos: `models/labels.json` contiene:
  - `class_names`: lista de clases (strings)
  - `img_size`: `[ancho, alto]` usado en el preprocesamiento.
  - `selected_model`: cadena con el modelo seleccionado tras comparativa.

## 4. Preprocesamiento

La imagen se redimensiona a `img_size`, se convierte a RGB y se aplica `preprocess_input` de Xception (si disponible). Se obtienen probabilidades softmax.

## 5. Límites y Notas

- NDVI/NDWI son aproximados porque no hay banda NIR real: solo fines exploratorios.
- Tamaño grande de imagen puede aumentar latencia; se recomienda ≤ 500KB por request si se usa base64.
- No se requiere autenticación.

## 6. Ejemplos (curl / PowerShell)

curl (Linux/macOS):

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST-SM4.jpeg/320px-HST-SM4.jpeg"}' \
  https://TU-SERVICIO.onrender.com/predict
```

PowerShell:

```powershell
$body = @{ image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST-SM4.jpeg/320px-HST-SM4.jpeg" } | ConvertTo-Json
Invoke-RestMethod -Uri https://TU-SERVICIO.onrender.com/predict -Method Post -Body $body -ContentType 'application/json'
```

## 7. Checklist rápida para QA

- [ ] /health responde 200 con status ok
- [ ] /predict con image_url válida devuelve 200 y `prediction`
- [ ] /predict con image_base64 válida devuelve 200
- [ ] /predict sin cuerpo válido devuelve 422
- [ ] Manejo de URL inválida devuelve 400
- [ ] Probabilities suma ≈ 1

---
Última actualización: ver control de versiones en el repositorio.
