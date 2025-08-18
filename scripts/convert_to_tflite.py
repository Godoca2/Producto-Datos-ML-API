"""Script para convertir el modelo Keras (.h5) a un modelo TFLite reducido.

Uso:
    python scripts/convert_to_tflite.py

Requisitos:
    - Archivo existente: models/xception_satellite.h5
Salida:
    - Archivo: models/xception_satellite.tflite (optimizado, posible float16)
"""
from pathlib import Path


def main():
    try:
        import tensorflow as tf  # type: ignore
    except Exception as e:
        raise SystemExit(f"TensorFlow no disponible: {e}")

    h5_path = Path('models/xception_satellite.h5')
    if not h5_path.exists():
        raise SystemExit(f"No se encuentra {h5_path}")

    print("Cargando modelo Keras...")
    model = tf.keras.models.load_model(h5_path)

    print("Convirtiendo a TFLite (Optimize.DEFAULT + intento float16)...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    try:
        converter.target_spec.supported_types = [tf.float16]
    except Exception:
        pass
    tflite_model = converter.convert()
    out_path = Path('models/xception_satellite.tflite')
    out_path.write_bytes(tflite_model)
    size_mb = out_path.stat().st_size / (1024*1024)
    print(f"Modelo TFLite escrito en {out_path} ({size_mb:.2f} MB)")


if __name__ == '__main__':
    main()
