# Resultados — Ejercicio 01: Dataset público y SVM reproducible

**Repositorio:** https://github.com/DAMB18/SVM-con-pipeline

Esta entrega integra dos desarrollos: LAB01 (ya realizado antes de esta unidad, dataset de cáncer de mama) y LAB02 (el desarrollado en esta práctica, dataset público de fuga de clientes). Ambos comparan un baseline (Dummy) contra un SVM sobre la misma partición train/test.

## Identificación de los datasets

### LAB01 — Breast Cancer Wisconsin (sklearn)

- **Fuente:** `sklearn.datasets.load_breast_cancer` — dataset de referencia incluido en scikit-learn (Breast Cancer Wisconsin Diagnostic, originalmente del UCI ML Repository).
- **Unidad de análisis:** muestra de biopsia de tejido mamario.
- **Target:** diagnóstico binario (maligno / benigno).
- **Notebook:** `notebooks/01_svm_giada.ipynb`.
- **Advertencia propia del notebook:** "Este ejemplo no constituye un diagnóstico médico".

### LAB02 — Iranian Churn Dataset (UCI)

- **Ficha:** https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset
- **Descarga:** https://archive.ics.uci.edu/static/public/563/iranian+churn+dataset.zip (ZIP público, sin autenticación)
- **Licencia:** CC BY 4.0.
- **Unidad de análisis:** cliente individual de una empresa de telecomunicaciones.
- **Target:** `Churn`, binario (1 = cancela el servicio, 0 = permanece), ~15.7% clase positiva.
- **Notebook:** `notebooks/02_churn_svm.ipynb`.
- **Procedencia, candidatos comparados, criterios de aceptación y diccionario completo:** `docs/ficha_dataset.md` y `docs/diccionario_datos.md`.

## Tabla principal de resultados

| Desarrollo | Modelo | F1 macro | Notas |
|---|---|---|---|
| LAB01 — Breast Cancer | Dummy (most_frequent) | 0.38 | baseline |
| LAB01 — Breast Cancer | SVM (rbf, C=1, gamma=scale) | 0.98 | antes de ajustar hiperparámetros |
| LAB01 — Breast Cancer | SVM + GridSearchCV, mejor combinación | 0.974 (validación cruzada, 5 folds) | C=10, gamma=0.01 — detalle en `reports/svm_cv_results.csv` |
| LAB02 — Churn | Dummy (most_frequent) | 0.457 | baseline |
| LAB02 — Churn | SVM (rbf, C=1, gamma=scale) | 0.841 | recall de la clase `Churn=1`: solo 0.58 (ver conclusión) |

## Figuras

- `reports/churn_confusion_matrix.png` — matriz de confusión del SVM de LAB02 sobre el conjunto de prueba.
- `reports/svm_best.joblib` — mejor modelo SVM de LAB01 (tras GridSearchCV), serializado.
- `reports/churn_svm_model.joblib` — modelo SVM de LAB02, serializado.
- `reports/svm_cv_results.csv` / `reports/churn_svm_results.csv` — tablas de resultados numéricos detalladas de cada desarrollo.

## Conclusión

Los dos desarrollos comparten el mismo esqueleto metodológico —partición estratificada, un baseline Dummy como piso de comparación, y un SVM dentro de un `Pipeline`— pero cuentan historias distintas sobre qué significa "un buen modelo". En LAB01, el salto de F1 macro de 0.38 a 0.98 es enorme porque el dataset de cáncer de mama es linealmente muy separable: es un problema casi de manual para SVM, y el ajuste con `GridSearchCV` apenas mueve la aguja (0.974 en validación cruzada), lo cual en sí mismo es una señal de que el modelo ya estaba cerca de su techo antes de tunear nada.

LAB02 es el caso más interesante para mí, precisamente porque el dataset no es de juguete: lo elegí, audité y documenté yo mismo, incluyendo un error propio que corregí en el camino (una fuente de terceros que traía columnas inventadas que no existen en el archivo oficial de UCI). Ahí el salto de 0.457 a 0.841 en F1 macro también es grande, pero el número que más me importa no es ese promedio: es que el recall de la clase `Churn=1` es apenas 0.58. Eso significa que, de cada 10 clientes que realmente se van a ir, el modelo solo detecta a 6. Y ese es exactamente el error que definí como más costoso en la ficha del dataset antes de entrenar nada: un falso negativo es un cliente que se pierde sin que el equipo de retención tenga oportunidad de intervenir.

Esta diferencia entre los dos desarrollos me deja una conclusión que va más allá de cualquiera de los dos datasets: un F1 macro alto no dice nada sobre si el modelo sirve para la decisión de negocio que se supone que debe apoyar. En LAB01 esa pregunta no aplicaba (es un ejercicio ilustrativo, no clínico, como aclara el propio notebook). Pero en LAB02, donde sí definí una decisión real —a quién contactar antes de que se vaya—, un accuracy de 93% y un F1 macro de 0.84 pueden esconder que casi la mitad de los clientes que se van pasan desapercibidos. La siguiente iteración razonable no es perseguir un F1 macro más alto en el grid search, sino priorizar explícitamente el recall de la clase de interés, por ejemplo con `class_weight="balanced"` o moviendo el umbral de decisión sobre `predict_proba`, y volver a evaluar con esa prioridad de negocio en mente desde el inicio, no como una corrección posterior.
