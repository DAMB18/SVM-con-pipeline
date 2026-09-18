import io
import zipfile
from pathlib import Path
from urllib.request import urlopen

import pandas as pd


def download_csv(url: str, destination="data/raw/dataset.csv") -> Path:
    if not url.startswith(("https://", "http://")):
        raise ValueError("La fuente debe ser una URL HTTP(S)")
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(url)
    if frame.empty:
        raise ValueError("El dataset descargado está vacío")
    frame.to_csv(path, index=False)
    return path


def download_iranian_churn_dataset(destination="data/raw/dataset.csv") -> Path:
    """Descarga el Iranian Churn Dataset (UCI) y lo guarda en `destination`.

    La fuente entrega un ZIP (no un CSV directo) y no requiere autenticación
    ni API key: es un archivo público servido por UCI. `destination` es una
    ruta relativa al directorio de trabajo del proyecto -- nunca una ruta
    absoluta de usuario (ej. C:\\Users\\... o /content/drive/...), para que
    el mismo código funcione en cualquier máquina.

    Ficha:    https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset
    Descarga: https://archive.ics.uci.edu/static/public/563/iranian+churn+dataset.zip
    """
    url = "https://archive.ics.uci.edu/static/public/563/iranian+churn+dataset.zip"
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)

    with urlopen(url, timeout=30) as response:
        raw_bytes = response.read()

    with zipfile.ZipFile(io.BytesIO(raw_bytes)) as zf:
        csv_names = [name for name in zf.namelist() if name.lower().endswith(".csv")]
        if not csv_names:
            raise ValueError("El ZIP descargado no contiene ningún archivo .csv")
        with zf.open(csv_names[0]) as csv_file:
            frame = pd.read_csv(csv_file)

    if frame.empty:
        raise ValueError("El dataset descargado está vacío")

    frame.to_csv(path, index=False)
    return path
