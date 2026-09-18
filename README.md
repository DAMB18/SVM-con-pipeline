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

## Conclusión

Elegí este dataset después de comparar dos candidatos documentados (UCI y OpenML) contra los seis criterios de aceptación de la práctica, y no me quedé con lo que decía la ficha oficial de UCI sin verificarlo: al abrir el CSV real encontré 16 columnas, no las 13 que UCI documenta. Investigué las tres columnas extra antes de decidir qué hacer con ellas, en vez de simplemente probarlas y quedarme con lo que diera mejor métrica. `FN` resultó ser una transformación lineal exacta de `Customer Value` (multiplicada por 0.9 en cada fila que revisé), `Age` resultó ser una repetición de `Age Group` con otra escala, y `FP` no tiene una definición que yo pueda verificar en ninguna fuente oficial. Las tres quedaron fuera del modelo por esas razones documentadas, no porque empeoraran el resultado.

También encontré que un 9.5% de las filas están duplicadas. Decidí no borrarlas sin evidencia de que sean un error, pero sí dejarlo anotado como un riesgo para la partición train/test, porque una fila repetida podría terminar filtrada entre ambos conjuntos sin que yo lo note.

Comparando el baseline contra el SVM, el salto en F1 macro es grande (aproximadamente 0.46 contra 0.84), lo que confirma que el modelo está aprendiendo algo real y no solo repitiendo la clase mayoritaria. Sin embargo, el número que más me importa para la decisión de negocio no es el F1 macro general, sino el recall de la clase `Churn=1`: con los hiperparámetros por defecto (`C=1`, `gamma="scale"`), el modelo detecta apenas alrededor del 58% de los clientes que realmente se van. El otro 42% son falsos negativos — exactamente el error que definí como más costoso en la ficha del dataset, porque significa clientes que se pierden sin que el equipo de retención tenga oportunidad de intervenir.

Esto me deja una conclusión clara para la siguiente iteración: no basta con optimizar el F1 macro o hacer grid search sobre `C` y `gamma` buscando el mejor promedio. El problema de negocio pide priorizar recall sobre precisión en la clase de interés, así que el siguiente paso razonable es probar `class_weight="balanced"` o mover el umbral de decisión sobre `predict_proba`, y volver a evaluar con esa prioridad explícita en mente, no con la métrica que más fácil sube.
