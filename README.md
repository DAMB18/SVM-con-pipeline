# INF-8239 — Unidad 1: Predicción de fuga de clientes (churn)

Proyecto de la Maestría en Ciencia de Datos II. Uso un dataset real de una empresa de telecomunicaciones para comparar un modelo baseline (Dummy) contra un SVM, siguiendo un flujo completo: selección justificada del dataset, auditoría de datos, retiro documentado de fugas/redundancias, pipeline de preprocesamiento y evaluación.

## Instalación

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Descarga del dataset

El dataset (Iranian Churn Dataset, UCI) se entrega como ZIP, no como CSV directo, y no requiere autenticación. La descarga está encapsulada en código — no depende de rutas de usuario como `C:\Users\...` ni de `/content/drive/...` — así que corre igual en cualquier máquina:

```powershell
python -c "from src.inf8239_u01.data import download_iranian_churn_dataset; print(download_iranian_churn_dataset())"
```

Esto guarda el CSV en `data/raw/dataset.csv` (ruta ignorada por git; ver `docs/descarga_datos.md` para el detalle del procedimiento).

## Target y métrica

- **Target:** `Churn` (1 = el cliente cancela el servicio, 0 = se queda). Ver la justificación completa de dominio, decisión y usuario en `docs/ficha_dataset.md`.
- **Métrica principal:** F1 macro, porque el target está desbalanceado (~84% / ~16%). También reviso `classification_report` por clase, porque el error que más me cuesta es el falso negativo (cliente que se va y el modelo no lo detecta), y eso no se ve en una métrica agregada.

## Ejecución

1. Descargar el dataset (paso anterior).
2. Correr `notebooks/02_churn_svm.ipynb` de principio a fin: carga, auditoría, definición de target/fugas, pipeline de preprocesamiento, baseline Dummy y SVM.
3. Correr las pruebas del contrato de datos:

```powershell
$env:PYTHONPATH="src"
python -m pytest -q
```

## Documentación del proyecto

- **Ficha de procedencia, licencia y comparación de candidatos:** `docs/ficha_dataset.md`
- **Procedimiento de descarga reproducible:** `docs/descarga_datos.md`
- **Diccionario de datos** (significado, unidad, fuente, disponibilidad, riesgo de cada columna, incluidas las 3 no documentadas por UCI que excluyo): `docs/diccionario_datos.md`
- **Notebook completo:** `notebooks/02_churn_svm.ipynb`
- **Pruebas del contrato de datos:** `tests/test_data_contract.py`

## LAB03 — Ensambles, reducción dimensional y Green AI

Extiende el ejercicio anterior **sin cambiar** el dataset, el target ni la partición train/test (mismo `random_state=42`, mismo `test_size=.20`): se reconstruyen igual al inicio de `notebooks/03_ensembles_pareto.ipynb` para poder comparar seis configuraciones de modelo sobre el mismo terreno.

- **Catálogo evaluado:** regresión logística, dos SVM (`C=1`, `C=10`), dos Random Forest (100 y 300 árboles) y un HistGradientBoosting — cada uno con 3 repeticiones de tiempo de ajuste (se reporta la mediana).
- **Resultados (`reports/green_ai_results.csv`):**

| Modelo | F1 macro | Recall (Churn=1) | Mediana ajuste (s) | Predicción (ms) | Tamaño (KB) | ¿Pareto? |
|---|---|---|---|---|---|---|
| boost | 0.943 | 0.909 | 0.144 | 5.6 | 316.7 | sí |
| rf_100 | 0.891 | 0.747 | 0.216 | 35.8 | 995.3 | no |
| svm_c10 | 0.886 | 0.697 | 0.244 | 12.5 | 62.5 | no |
| rf_300 | 0.884 | 0.737 | 0.600 | 77.3 | 2971.9 | no |
| svm_c1 | 0.806 | 0.495 | 0.262 | 15.3 | 78.0 | no |
| logistic | 0.750 | 0.424 | 0.012 | 2.4 | 4.1 | sí |

- **PCA:** con 95% de varianza retenida se queda con 8 de las 14 columnas; el F1 macro del SVM apenas baja de 0.806 a 0.799 — casi todo lo útil ya vive en ese subespacio.
- **t-SNE (`reports/tsne_two_seeds.png`):** dos mapas con semillas distintas (42 y 7). La estructura gruesa (el cluster compacto de clientes que se van) se mantiene entre semillas; lo que cambia es la orientación y algunos detalles finos — la separación visual no prueba por sí sola que un clasificador vaya a funcionar bien.
- **Frontera de Pareto (`reports/pareto.png`, `src/inf8239_u01/green.py::pareto_flags`):** solo `boost` y `logistic` quedan sin dominar. Elijo **`boost`**, no la alternativa más barata (`logistic`): pagar 0.144 s en vez de 0.012 s es un costo trivial en términos absolutos, y a cambio se gana 0.193 de F1 macro y, sobre todo, se pasa de detectar 42% a 91% de los clientes que realmente se van — el error que definí como más costoso desde la ficha del dataset. El análisis completo (300-500 palabras, con las limitaciones de medir tiempo como proxy de costo computacional y no como consumo energético) está en `notebooks/03_ensembles_pareto.ipynb`.
- **Entorno registrado:** versión de Python, sistema operativo y versión de scikit-learn, impresos al final del notebook (paso 9), porque el tiempo medido es contextual a la máquina donde se corre.
- **Pruebas:** `tests/test_green.py` cubre `pareto_flags` (fila dominada, un solo modelo, modelo más rápido y mejor domina, filas empatadas).
- Nota: igual que en LAB02, los `.joblib` de `reports/models/` no se versionan en git (`.gitignore` tiene `*.joblib`); existen localmente donde se corrió el notebook.

## Conclusión

Elegí este dataset después de comparar dos candidatos documentados (UCI y OpenML) contra los seis criterios de aceptación de la práctica, y no me quedé con lo que decía la ficha oficial de UCI sin verificarlo. De hecho, mi primera verificación tuvo un error que vale la pena dejar anotado: exploré una copia del dataset en un repositorio de GitHub de un tercero, no la descarga oficial, y esa copia traía dos columnas de más (`FN`, `FP`) que ese usuario había agregado por su cuenta — `FN` resultó ser una transformación lineal exacta de `Customer Value`. Cuando corrí la descarga oficial de UCI para el proyecto real, esas dos columnas no existen: el archivo real tiene 14 columnas, no 16. Sí se confirmó que `Age` es una repetición de `Age Group` con otra escala, y esa la excluyo del modelo por esa razón documentada, no porque empeorara el resultado. La lección que me llevo es auditar siempre el archivo que realmente se va a usar en el proyecto, no una copia de un tercero aunque parezca la misma fuente.

También encontré que un 9.5% de las filas están duplicadas. Decidí no borrarlas sin evidencia de que sean un error, pero sí dejarlo anotado como un riesgo para la partición train/test, porque una fila repetida podría terminar filtrada entre ambos conjuntos sin que yo lo note.

Comparando el baseline contra el SVM, el salto en F1 macro es grande (aproximadamente 0.46 contra 0.84), lo que confirma que el modelo está aprendiendo algo real y no solo repitiendo la clase mayoritaria. Sin embargo, el número que más me importa para la decisión de negocio no es el F1 macro general, sino el recall de la clase `Churn=1`: con los hiperparámetros por defecto (`C=1`, `gamma="scale"`), el modelo detecta apenas alrededor del 58% de los clientes que realmente se van. El otro 42% son falsos negativos — exactamente el error que definí como más costoso en la ficha del dataset, porque significa clientes que se pierden sin que el equipo de retención tenga oportunidad de intervenir.

Esto me deja una conclusión clara para la siguiente iteración: no basta con optimizar el F1 macro o hacer grid search sobre `C` y `gamma` buscando el mejor promedio. El problema de negocio pide priorizar recall sobre precisión en la clase de interés, así que el siguiente paso razonable es probar `class_weight="balanced"` o mover el umbral de decisión sobre `predict_proba`, y volver a evaluar con esa prioridad explícita en mente, no con la métrica que más fácil sube.
