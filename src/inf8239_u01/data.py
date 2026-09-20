import io
import zipfile
from pathlib import Path
from urllib.request import urlopen

import pandas as pd

# Raíz del proyecto, calculada desde la ubicación de este archivo
# (src/inf8239_u01/data.py) y no desde el directorio de trabajo de quien
# lo llama. Esto es importante porque un notebook en notebooks/ y un
# comando `python -c` corrido desde la raíz del repo tienen cwd distinto;
# si el destino por defecto fuera un string relativo como "data/raw/...",
# cada uno guardaría el CSV en un lugar distinto sin que nadie se diera
# cuenta. Al anclarlo aquí, siempre cae en el mismo sitio real del repo.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW_PATH = PROJECT_ROOT / "data" / "raw" / "dataset.csv"


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


def download_iranian_churn_dataset(destination=None) -> Path:
    """Descarga el Iranian Churn Dataset (UCI) y lo guarda en `destination`.

    La fuente entrega un ZIP (no un CSV directo) y no requiere autenticación
    ni API key: es un archivo público servido por UCI. Si no se pasa
    `destination`, se usa `DEFAULT_RAW_PATH` (`data/raw/dataset.csv` anclado
    a la raíz del proyecto) -- nunca una ruta absoluta de usuario (ej.
    C:\\Users\\... o /content/drive/...), para que el mismo código funcione
    igual desde una terminal en la raíz del repo o desde un notebook en
    notebooks/ (que en este proyecto corre con otro directorio de trabajo).

    Ficha:    https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset
    Descarga: https://archive.ics.uci.edu/static/public/563/iranian+churn+dataset.zip
    """
    url = "https://archive.ics.uci.edu/static/public/563/iranian+churn+dataset.zip"
    path = Path(destination) if destination is not None else DEFAULT_RAW_PATH
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
