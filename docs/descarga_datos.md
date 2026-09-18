# Procedimiento de descarga del dataset

## Fuente y tipo de acceso

**Candidato A — UCI: Iranian Churn Dataset**

- Ficha: https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset
- Descarga: https://archive.ics.uci.edu/static/public/563/iranian+churn+dataset.zip
- Formato de entrega: **ZIP estático** (41 KB) con un archivo `.csv` adentro.
- Autenticación: **No requiere** API key, login ni cuenta — es un archivo público servido directamente por UCI.

Como la fuente entrega un ZIP y no un CSV directo, el procedimiento de
descarga queda **encapsulado en código** en vez de descargarse manualmente y
copiarse a mano al proyecto: la función
[`download_iranian_churn_dataset`](../src/inf8239_u01/data.py) en
`src/inf8239_u01/data.py` descarga el ZIP en memoria, lo abre con
`zipfile`, localiza el `.csv` que contiene, lo carga con `pandas` y lo
guarda en `data/raw/dataset.csv`.

Esto complementa a la función `download_csv(url, destination)` ya existente
en el mismo módulo, que sirve para fuentes que entregan un CSV directo (por
ejemplo, si más adelante se usa el Candidato B vía una URL de exportación
CSV de OpenML).

## Por qué no se usan rutas absolutas de usuario

Ninguna de las dos funciones usa rutas como:

- `C:\Users\alexb\Desktop\...` (específica de esta máquina Windows)
- `/content/drive/MyDrive/...` (específica de un notebook en Google Colab)

El parámetro `destination` tiene como valor por defecto `data/raw/dataset.csv`,
una ruta **relativa** al directorio desde donde se ejecuta el código. Así,
el dataset siempre cae en el mismo lugar dentro del repositorio sin importar
la computadora, el sistema operativo o el entorno (local, Colab, CI) donde
se corra.

`data/raw/` está en `.gitignore` (solo se versiona `data/raw/.gitkeep`), por
lo que los datos crudos nunca se suben al repositorio — se regeneran
localmente llamando a la función.

## Cómo ejecutarlo

Desde la raíz del repositorio, con el entorno virtual activado:

```powershell
python -c "from inf8239_u01.data import download_iranian_churn_dataset; print(download_iranian_churn_dataset())"
```

O, dentro de una notebook (por ejemplo `00_verificacion.ipynb`):

```python
from inf8239_u01.data import download_iranian_churn_dataset

ruta = download_iranian_churn_dataset()
print(f"Dataset listo en: {ruta}")
```

## Si en el futuro se usa el Candidato B (OpenML)

OpenML expone una API (paquete `openml` de Python) en vez de un ZIP
estático. El mismo principio aplicaría: el acceso se encapsularía en una
función análoga (por ejemplo `download_telco_churn_dataset` en
`src/inf8239_u01/data.py`) que use `openml.datasets.get_dataset(42178)` y
guarde el resultado también en `data/raw/`, sin rutas de usuario
hardcodeadas ni credenciales en el código (OpenML permite descargar
datasets públicos sin API key).
