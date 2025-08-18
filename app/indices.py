from typing import Tuple
import numpy as np
from PIL import Image


def calcular_ndvi_from_rgb(img: Image.Image) -> float:
    # Aproximación usando canal rojo como proxy NIR (limitación de RGB)
    arr = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    red = arr[:, :, 0]
    nir = red  # proxy
    ndvi = (nir - red) / (nir + red + 1e-6)
    return float(np.mean(ndvi))


def calcular_ndwi_from_rgb(img: Image.Image) -> float:
    arr = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    green = arr[:, :, 1]
    nir = arr[:, :, 2]
    ndwi = (green - nir) / (green + nir + 1e-6)
    return float(np.mean(ndwi))


def calcular_indices(img: Image.Image) -> Tuple[float, float]:
    return calcular_ndvi_from_rgb(img), calcular_ndwi_from_rgb(img)
