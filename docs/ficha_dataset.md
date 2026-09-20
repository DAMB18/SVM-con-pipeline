# Ficha del dataset

- Dominio: Negocio / telecomunicaciones — retención de clientes (customer churn)
- Unidad de análisis: Cliente individual (suscriptor de un servicio de telecomunicaciones)
- Decisión: Si la empresa debe intervenir con una acción de retención (descuento, llamada proactiva, oferta) sobre un cliente específico antes de que cancele el servicio
- Target: Churn — variable binaria (1 = el cliente cancela el servicio, 0 = el cliente permanece)
- Tipo de tarea: Clasificación binaria supervisada
- Error más costoso: Falso negativo — no detectar a tiempo a un cliente que sí va a cancelar. Se pierde la oportunidad de retenerlo, y el costo de readquirir un cliente nuevo suele ser mayor que el costo de una campaña de retención mal dirigida (falso positivo).
- Usuario de la solución: Equipo de retención / marketing de la empresa, que usa el modelo para priorizar a qué clientes contactar con campañas de retención

## Comparación de candidatos

| Criterio | Candidato A — UCI: Iranian Churn Dataset | Candidato B — OpenML: telco-customer-churn |
|---|---|---|
| Procedencia | UCI Machine Learning Repository. Datos de una empresa telefónica iraní, recolectados durante 12 meses. Donado el 8 abr 2020. | OpenML (dataset ID 42178), subido por Andreas Mueller el 15 oct 2019. Basado en el conjunto IBM Telco Customer Churn. |
| Licencia | CC BY 4.0 | Marcada como "Public" en OpenML — verificar términos exactos, ya que el dataset original de IBM tiene su propia licencia de datos de muestra |
| Filas/columnas | 3,150 filas × 13 atributos + target | 7,043 filas × 20 atributos + target |
| Target y clases | `Churn` binario (0/1). Clase minoritaria (churn) ronda ~15% | `Churn` binario (Yes/No). Distribución 73.5% / 26.5% |
| Ausentes | Ninguno reportado | 0 reportados en metadata de OpenML — pero en la versión original (IBM/Kaggle) la columna `TotalCharges` trae 11 valores en blanco; verificar al descargar |
| Riesgo de fuga | Bajo-medio: los atributos son datos agregados de los primeros 9 meses, y la etiqueta de churn corresponde al mes 12 (ventana de 3 meses). Aun así, confirmar que ninguna variable derive directamente del evento de churn. | Medio: no hay ventana temporal explícita documentada entre atributos y el evento de churn. Revisar si `tenure` o `TotalCharges` (que es `MonthlyCharges × tenure`) introducen fuga o multicolinealidad problemática. |
| URL ficha | https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset | https://www.openml.org/d/42178 |
| URL descarga | https://archive.ics.uci.edu/static/public/563/iranian+churn+dataset.zip (ZIP de 41 KB con el CSV) | Botón de descarga ARFF/CSV/Parquet en la página de OpenML (dataset ID 42178) |

## Criterios de aceptación aplicados al Candidato A (elegido)

Ya descargué el CSV del Candidato A y lo inspeccioné antes de decidir, no me quedé solo con lo que dice la ficha de UCI. Así quedó cada criterio:

- **Al menos 500 filas, salvo autorización**: cumple. Son 3,150 filas, muy por encima del mínimo.
- **Target observable y mínimo dos clases**: cumple. `Churn` es binario (0 = no fuga, 1 = fuga), con 2,655 casos en 0 y 495 en 1. Sí está desbalanceado (~15.7% de fuga), lo cual voy a tener en cuenta al elegir la métrica (por eso uso F1 macro y no accuracy a secas).
- **Datos permitidos para uso académico**: cumple. La licencia es CC BY 4.0, que permite uso y redistribución con atribución — no hay restricción para un trabajo de curso.
- **Variables disponibles al momento de predecir**: aquí encontré algo que no esperaba, y también un error mío que corregí. En mi primera exploración usé una copia de este dataset en un repositorio de GitHub de un tercero (no la descarga oficial), y esa copia traía 16 columnas con dos de más (`FN`, `FP`) que ese usuario había agregado por su cuenta. Al correr la descarga oficial de UCI (`download_iranian_churn_dataset()`), el archivo real tiene **14 columnas**: las 13 documentadas por UCI más `Age`, que sí viene en el archivo pero no aparece listada en la tabla de variables oficial. Documento esto en `docs/diccionario_datos.md` y excluyo `Age` en el paso 7 por ser redundante con `Age Group`.
- **Tamaño compatible con CPU/Colab gratuito**: cumple sin problema. Son 3,150 filas × 14 columnas (~180 KB en memoria), entrena en segundos en CPU.
- **No repetir dataset con otro estudiante sin autorización**: pendiente de confirmar con el resto del curso — lo reviso antes de la entrega final.

**Aprobación docente**: según lo acordado, ya cuento con la aprobación del docente para este dataset, así que continúo con el resto de la práctica.
