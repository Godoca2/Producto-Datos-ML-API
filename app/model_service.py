import base64
import io
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

from PIL import Image
import numpy as np


class ModelService:
    def __init__(self, class_names: Optional[list[str]] = None, img_size: tuple[int, int] = (150, 150)):
        """Inicializa el servicio de modelo."""
        # Puede ser un modelo Keras, el string "dummy" o un intérprete TFLite
        self.model: Optional[Union[str, "KerasModelWrapper", "TFLiteModelWrapper"]] = None
        self.class_names = class_names or ["class_0", "class_1"]
        self.img_size = img_size
        self._tf = None  # carga perezosa de tensorflow
        self._is_tflite = False

    def _try_import_tf(self):
        if self._tf is None:
            try:
                import tensorflow as tf  # type: ignore

                self._tf = tf
            except Exception:
                self._tf = None
        return self._tf

    def load(self, path: Optional[str] = None) -> None:
        """
        Intenta cargar el modelo y labels desde disco.
        - Modelo: models/xception_satellite.h5 (o ruta provista)
        - Labels: models/labels.json con {"class_names": [...], "img_size": [w,h]}
        Si falla, mantiene un modelo dummy.
        """
        models_dir = Path("models")
        labels_path = models_dir / "labels.json"
        # Intentamos primero un modelo TFLite si existe; si no, .h5
        if path:
            model_path = Path(path)
        else:
            tflite_candidate = models_dir / "xception_satellite.tflite"
            model_path = tflite_candidate if tflite_candidate.exists() else models_dir / "xception_satellite.h5"

        # Cargar labels si existen
        if labels_path.exists():
            try:
                meta = json.loads(labels_path.read_text(encoding="utf-8"))
                if isinstance(meta.get("class_names"), list):
                    self.class_names = [str(c) for c in meta["class_names"]]
                if isinstance(meta.get("img_size"), (list, tuple)) and len(meta["img_size"]) == 2:
                    self.img_size = (int(meta["img_size"][0]), int(meta["img_size"][1]))
            except Exception:
                pass

        # Cargar modelo Keras si existe y TF disponible
        if model_path.exists():
            if model_path.suffix == ".tflite":
                tf = self._try_import_tf()
                if tf is not None:
                    try:
                        self.model = TFLiteModelWrapper(str(model_path), tf)
                        self._is_tflite = True
                    except Exception:
                        self.model = "dummy"
                else:
                    self.model = "dummy"
            else:
                tf = self._try_import_tf()
                if tf is not None:
                    try:
                        self.model = KerasModelWrapper(tf.keras.models.load_model(model_path))  # type: ignore[attr-defined]
                    except Exception:
                        self.model = "dummy"
                else:
                    self.model = "dummy"
        else:
            self.model = "dummy"

    def _preprocess(self, image: Image.Image) -> np.ndarray:
        image = image.convert("RGB").resize(self.img_size)
        arr = np.asarray(image, dtype=np.float32)
        # Intentar usar preprocess_input de Xception si existe
        try:
            tf = self._try_import_tf()
            if tf is not None:
                from tensorflow.keras.applications.xception import preprocess_input  # type: ignore

                arr = preprocess_input(arr)
            else:
                arr = arr / 255.0
        except Exception:
            arr = arr / 255.0
        # (h,w,3) -> (1,h,w,3)
        arr = np.expand_dims(arr, axis=0)
        return arr

    def predict(self, image: Image.Image) -> Dict[str, Any]:
        x = self._preprocess(image)
        if self.model is not None and self.model != "dummy":
            if isinstance(self.model, KerasModelWrapper):
                preds = self.model.predict(x)[0]
            elif isinstance(self.model, TFLiteModelWrapper):
                preds = self.model.predict(x)[0]
            else:
                preds = self._dummy_probs()
        else:
            preds = self._dummy_probs()

        pred_idx = int(np.argmax(preds))
        return {
            "prediction": self.class_names[pred_idx] if self.class_names else str(pred_idx),
            "probabilities": {self.class_names[i]: float(p) for i, p in enumerate(preds)},
        }

    def _dummy_probs(self) -> np.ndarray:
        n = len(self.class_names)
        preds = np.full((n,), 1.0 / n, dtype=np.float32)
        if n:
            preds[0] = min(0.8, preds[0] + 0.5)
        preds = preds / preds.sum()
        return preds


def load_image_from_base64(b64data: str) -> Image.Image:
    data = base64.b64decode(b64data)
    return Image.open(io.BytesIO(data))


class KerasModelWrapper:
    def __init__(self, model):
        self._model = model

    def predict(self, x: np.ndarray) -> np.ndarray:
        return self._model.predict(x)


class TFLiteModelWrapper:
    def __init__(self, path: str, tf_module):
        # Creamos e inicializamos intérprete TFLite
        self.interpreter = tf_module.lite.Interpreter(model_path=path)
        self.interpreter.allocate_tensors()
        details_in = self.interpreter.get_input_details()
        details_out = self.interpreter.get_output_details()
        self.input_index = details_in[0]["index"]
        self.output_index = details_out[0]["index"]
        self._input_dtype = details_in[0]["dtype"]

    def predict(self, x: np.ndarray) -> np.ndarray:
        # Adaptar dtype
        xin = x.astype(self._input_dtype, copy=False)
        self.interpreter.set_tensor(self.input_index, xin)
        self.interpreter.invoke()
        out = self.interpreter.get_tensor(self.output_index)
        return out
