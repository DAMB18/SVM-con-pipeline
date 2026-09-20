# Resultados — Ejercicio 02: Ensambles, reducción dimensional y Green AI

**Repositorio:** https://github.com/DAMB18/SVM-con-pipeline (tag `u01-ejercicio02`, commit `c587ff3c`)

Esta entrega integra las evidencias de LAB03 (`notebooks/03_ensembles_pareto.ipynb`), que amplía el Ejercicio 01 sin cambiar el dataset, el target ni la partición aprobados ahí: reutilizo exactamente el mismo `TARGET="Churn"`, `DROP_COLUMNS=["Age"]`, el mismo `preprocess` y el mismo `train_test_split(test_size=.20, random_state=42, stratify=y)` de `notebooks/02_churn_svm.ipynb`.

## Identificación del dataset

- **Nombre:** Iranian Churn Dataset (UCI Machine Learning Repository).
- **Ficha:** https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset
- **Descarga:** https://archive.ics.uci.edu/static/public/563/iranian+churn+dataset.zip (ZIP público, sin autenticación; encapsulada en `src/inf8239_u01/data.py::download_iranian_churn_dataset`).
- **Licencia:** CC BY 4.0.
- **Unidad de análisis:** cliente individual de una empresa de telecomunicaciones (3,150 filas, 14 columnas tras retirar `Age` por redundancia con `Age Group`).
- **Target:** `Churn`, binario (1 = cancela el servicio, 0 = permanece), ~15.7% clase positiva.
- **Partición:** 2,520 filas de entrenamiento / 630 de prueba, estratificada, `random_state=42` — idéntica a la de LAB02/Ejercicio 01.
- **Procedencia, candidatos comparados, criterios de aceptación y diccionario completo:** `docs/ficha_dataset.md` y `docs/diccionario_datos.md`.

## Tabla principal de resultados

Seis configuraciones, medidas con 3 repeticiones de ajuste (se reporta la mediana) y una corrida de inferencia sobre el conjunto de prueba:

| Modelo | Familia | F1 macro | Recall (Churn=1) | Mediana ajuste (s) | Inferencia (ms) | Tamaño (KB) | ¿Pareto? |
|---|---|---|---|---|---|---|---|
| boost | HistGradientBoosting | 0.943 | 0.909 | 0.144 | 5.6 | 316.7 | **sí** |
| rf_100 | Random Forest (100 árboles) | 0.891 | 0.747 | 0.216 | 35.8 | 995.3 | no |
| svm_c10 | SVM (C=10) | 0.886 | 0.697 | 0.244 | 12.5 | 62.5 | no |
| rf_300 | Random Forest (300 árboles) | 0.884 | 0.737 | 0.600 | 77.3 | 2971.9 | no |
| svm_c1 | SVM (C=1) | 0.806 | 0.495 | 0.262 | 15.3 | 78.0 | no |
| logistic | Regresión logística | 0.750 | 0.424 | 0.012 | 2.4 | 4.1 | **sí** |

Fuente: `reports/green_ai_results.csv`.

**PCA:** con 95% de varianza retenida, el SVM se queda con 8 de las 14 columnas numéricas y su F1 macro baja de 0.806 a 0.799 (diferencia de 0.007) — casi todo lo útil para clasificar ya vive en ese subespacio de menor dimensión.

## Figuras

- `reports/pareto.png` — F1 macro vs. mediana de tiempo de ajuste, con los dos modelos no dominados (`boost`, `logistic`) resaltados.
- `reports/tsne_two_seeds.png` — dos proyecciones t-SNE (semillas 42 y 7) sobre una muestra de 1,000 clientes; la estructura gruesa (el cluster compacto de clientes que se van) se mantiene entre semillas, y lo que cambia es la orientación y algunos detalles finos del embedding — no es evidencia de causalidad ni sustituye la evaluación real del modelo.
- `reports/green_ai_results.csv` — tabla numérica completa de las seis configuraciones.
- `reports/models/*.joblib` — los seis modelos serializados (gitignorados por `*.joblib`, igual que en Ejercicio 01; existen localmente donde se corrió el notebook).

## Pruebas

`tests/test_green.py` cubre `pareto_flags` (`src/inf8239_u01/green.py`) con cuatro casos: una fila dominada, un único modelo, un modelo que domina en ambas dimensiones a la vez, y filas empatadas. `python -m pytest -q` da 12 pruebas en verde en total (las 8 de Ejercicio 01 más estas 4).

## Conclusión — defensa de la decisión Pareto

Con las seis configuraciones evaluadas, la frontera de Pareto entre F1 macro y mediana de tiempo de ajuste queda formada por solo dos modelos: boost (HistGradientBoosting) y logistic (regresión logística). Los otros cuatro —rf_100, svm_c10, rf_300 y svm_c1— quedan estrictamente dominados: existe al menos otro modelo (boost) que logra un F1 macro más alto y un tiempo de ajuste más bajo al mismo tiempo, así que no tiene sentido elegirlos bajo ningún balance razonable entre desempeño y costo.

El F1 macro máximo lo obtiene boost, con 0.943, casi diez puntos por encima del segundo mejor no dominado por él (rf_100, 0.891). Lo que hace interesante a boost no es solo ese máximo, sino que lo logra con una mediana de ajuste de apenas 0.144 s, más rápida que las dos variantes de SVM y que ambos Random Forest — es decir, domina en las dos dimensiones a la vez a cuatro de los cinco competidores restantes.

La alternativa más barata en la frontera es logistic: 0.012 s de mediana de ajuste, un 91.7% menos tiempo que boost, y el modelo serializado más liviano con diferencia (4.1 KB contra 316.7 KB de boost). Pero esa economía tiene un costo real en la métrica que definí como prioritaria desde la ficha del dataset: el recall de la clase Churn=1. logistic detecta solo el 42% de los clientes que realmente se van (recall_churn=0.424), mientras que boost detecta el 91% (0.909). La diferencia absoluta de F1 macro entre ambos es de 0.193 puntos, y en términos del error más costoso del proyecto —el falso negativo de retención— logistic deja sin detectar más de la mitad de los clientes que se van, contra menos de una décima parte con boost.

Mi decisión es quedarme con boost, no con la opción más barata de la frontera. La razón es de contexto de negocio, no solo de números: 0.144 s de ajuste y 316 KB de modelo son costos triviales en términos absolutos para un proceso de scoring que corre, como mucho, una vez al día sobre unos pocos miles de clientes; el ahorro de 91.7% de tiempo que ofrece logistic no compensa perder más de la mitad del recall sobre la clase que me importa.

Limitaciones: estas medidas de tiempo y tamaño son proxies de costo computacional, no consumo energético ni huella de CO2 —no medí ninguna de las dos, y no las voy a presentar como si lo hubiera hecho—. Los tiempos además son relativos a esta máquina y a esta única corrida (Linux x86_64, scikit-learn 1.8.0, sin otros procesos compitiendo por CPU); en el hardware del alumno, o bajo carga distinta, la magnitud absoluta cambiaría aunque el orden relativo entre modelos probablemente se mantenga.

## Verificación contra la rúbrica

| Criterio | Puntos | Evidencia |
|---|---|---|
| Comparación homogénea de al menos seis configuraciones | 1.0 | `notebooks/03_ensembles_pareto.ipynb` (paso 2-3), `reports/green_ai_results.csv`: logistic, svm_c1, svm_c10, rf_100, rf_300, boost, todas sobre el mismo `Xtr/Xte/ytr/yte`. |
| PCA y dos visualizaciones t-SNE interpretadas | 1.0 | Paso 4 (PCA, 8/14 componentes, comparación de F1) y paso 5 (t-SNE semillas 42/7, `reports/tsne_two_seeds.png`) con lectura explícita de qué permanece/cambia y la advertencia de no-causalidad. |
| Medición repetida de tiempo, inferencia y tamaño | 1.0 | Paso 3: 3 repeticiones de `fit` (mediana reportada), tiempo de `predict` en ms y tamaño del `.joblib` en KB por modelo. |
| Frontera Pareto y decisión cuantificada | 1.5 | `src/inf8239_u01/green.py::pareto_flags` + `reports/pareto.png` + análisis de 449 palabras (arriba) con F1 máximo, alternativa, diferencia absoluta, ahorro porcentual, diferencia de tamaño, limitaciones y contexto de hardware. |
| Pruebas, README, CSV, figuras y Git | 0.5 | `tests/test_green.py` (4 casos), sección "LAB03" en `README.md`, `reports/green_ai_results.csv`, `reports/pareto.png` + `reports/tsne_two_seeds.png`, commit `c587ff3c` y tag `u01-ejercicio02` en GitHub. |

**Nota de limpieza pendiente:** el repositorio remoto tiene actualmente una carpeta `Claude outputs/` con una copia duplicada de `resultados_ejercicio01.pdf` que se coló en el commit `c587ff3c` por un `git add .` — no forma parte de la estructura pedida (`notebooks`, `src`, `tests`, `reports`, `requirements.txt`, `README.md`) y conviene retirarla antes de la entrega final.
