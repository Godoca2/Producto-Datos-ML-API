# Guía de Despliegue en Render

## Pasos para Desplegar en Render

### 1. Crear cuenta en Render
- Ve a [render.com](https://render.com) y crea una cuenta
- Conecta tu cuenta de GitHub

### 2. Crear Web Service
1. Click en "New +" → "Web Service"
2. Conecta tu repositorio: `Godoca2/Producto-Datos-ML-API`
3. Configura los siguientes campos:

**Basic Settings:**
- **Name:** `producto-datos-ml-api` (o el que prefieras)
- **Region:** Oregon (US West) o la más cercana
- **Branch:** `main`
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Plan:**
- Selecciona "Free" para desarrollo/demo

### 3. Variables de Entorno (Opcionales)
En la sección Environment Variables, puedes añadir:

```
TF_CPP_MIN_LOG_LEVEL=2
PYTHONUNBUFFERED=1
```

### 4. Deploy
- Click "Create Web Service"
- Render automáticamente:
  1. Clona el repositorio
  2. Instala dependencias desde `requirements.txt`
  3. Ejecuta el comando de inicio
  4. Asigna una URL pública

### 5. Verificar Despliegue
Una vez completado el deploy (5-10 minutos):

1. **Health Check:**
   - GET `https://tu-servicio.onrender.com/health`
   - Debe devolver: `{"status": "ok", "version": "0.1.0"}`

2. **API Documentation:**
   - Ve a `https://tu-servicio.onrender.com/docs`
   - Swagger UI con documentación interactiva

3. **Test Prediction:**
   ```bash
   curl -X POST "https://tu-servicio.onrender.com/predict" \
        -H "Content-Type: application/json" \
        -d '{"image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST-SM4.jpeg/320px-HST-SM4.jpeg"}'
   ```

### 6. Actualizar README
Una vez desplegado, actualiza `README.md` con la URL real:

```markdown
## URL Despliegue (Render)

🚀 **API en vivo:** https://tu-servicio.onrender.com

- Health: https://tu-servicio.onrender.com/health
- Docs: https://tu-servicio.onrender.com/docs
```

## Notas Importantes

### Modelo ML
- El servicio funciona sin el modelo .h5 (usa modo "dummy")
- Para usar modelo real: subir `models/xception_satellite.tflite` (<100MB)
- El archivo `.h5` original (162MB) está excluido por límites de GitHub

### Rendimiento
- **Plan Free:** Limitado a 512MB RAM, se duerme tras 15 min de inactividad
- **Primera carga:** Puede tardar ~30s en "despertar"
- **Upgrade:** Para uso productivo considera plan "Starter" ($7/mes)

### Monitoreo
- Logs disponibles en Render Dashboard
- Healthchecks automáticos en `/health`
- Métricas básicas en el panel de Render

## Solución de Problemas

### Build Failed
- Verificar `requirements.txt` tiene todas las dependencias
- Revisar logs de build en Render Dashboard

### Service Not Starting
- Verificar comando de inicio: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Revisar logs de runtime

### Import Errors
- Verificar estructura de proyecto en repo
- Asegurar que `app/` contiene `__init__.py`

### Out of Memory
- Reducir dependencias o cambiar a plan con más RAM
- El modelo TensorFlow puede consumir ~200-300MB
