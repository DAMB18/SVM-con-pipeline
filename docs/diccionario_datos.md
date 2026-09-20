# Diccionario de datos — Iranian Churn Dataset

Fuente: [ficha UCI](https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset) · Datos de una empresa de telecomunicaciones iraní, recolectados durante 12 meses. 3,150 filas, sin valores ausentes.

Nota personal (y corrección): en mi primera exploración usé una copia de este dataset en un repositorio de GitHub de un tercero, no la descarga oficial de UCI, y esa copia traía **16 columnas** (dos de más, `FN` y `FP`, que ese usuario agregó por su cuenta — comprobé que `FN` era simplemente `Customer Value × 0.9`). Una vez que corrí `download_iranian_churn_dataset()` contra la URL oficial de UCI, el archivo real tiene **14 columnas**: las 13 documentadas (12 atributos + `Churn`) más `Age`, que sí viene en el archivo oficial aunque la tabla de variables de UCI no la liste aparte. Dejo esto anotado como lección: para la ficha y el diccionario hay que auditar el archivo que efectivamente se va a usar, no una copia de terceros, aunque parezca la misma fuente.

## Columnas documentadas por UCI

| Columna | Significado | Unidad / rango | Fuente | Momento de disponibilidad | Transformación prevista | Riesgo |
|---|---|---|---|---|---|---|
| `Call  Failure` | Número de llamadas fallidas | Entero, conteo | Sistema del operador | Disponible antes de la fuga (acumulado histórico) | Ninguna; entra numérica al pipeline | Bajo |
| `Complains` | Si el cliente presentó alguna queja | Binario 0/1 | Sistema de atención al cliente | Disponible antes de la fuga | Ninguna | Bajo |
| `Subscription  Length` | Meses totales de suscripción | Entero, meses | Sistema de facturación | Disponible antes de la fuga | Ninguna | Bajo |
| `Charge  Amount` | Monto cobrado, codificado como ordinal | Entero 0 (más bajo) a 9 (más alto) | Sistema de facturación | Disponible antes de la fuga | Ninguna (ya es ordinal) | Bajo |
| `Seconds of Use` | Segundos totales de llamadas | Entero, segundos | Sistema del operador | Disponible antes de la fuga | Ninguna | Bajo |
| `Frequency of use` | Número total de llamadas | Entero, conteo | Sistema del operador | Disponible antes de la fuga | Ninguna | Bajo |
| `Frequency of SMS` | Número total de mensajes de texto | Entero, conteo | Sistema del operador | Disponible antes de la fuga | Ninguna | Bajo |
| `Distinct Called Numbers` | Cantidad de números distintos llamados | Entero, conteo | Sistema del operador | Disponible antes de la fuga | Ninguna | Bajo |
| `Age Group` | Grupo etario del cliente | Ordinal 1 (más joven) a 5 (mayor) | Datos de registro del cliente | Disponible antes de la fuga | Ninguna (ya es ordinal) | Bajo |
| `Tariff Plan` | Tipo de plan | 1 = prepago, 2 = contrato | Sistema de facturación | Disponible antes de la fuga | Ninguna | Bajo |
| `Status` | Estado de la cuenta | 1 = activo, 2 = no activo | Sistema del operador | Disponible antes de la fuga | Ninguna | Medio — hay que confirmar que "no activo" no sea, en la práctica, casi lo mismo que el propio churn (podría ser casi la misma información con otro nombre) |
| `Customer Value` | Valor calculado del cliente (métrica interna de la empresa) | Numérico, continuo | Calculado por el operador | Disponible antes de la fuga | Ninguna | Bajo |
| `Churn` | **Target.** Si el cliente se fue o no | Binario: 1 = fuga, 0 = no fuga | Definido por la empresa al cierre del período | Es el resultado, no un predictor | — | — |

## Columna presente en el archivo oficial pero no documentada por UCI

| Columna | Lo que encontré al auditarla | Decisión |
|---|---|---|
| `Age` | Solo tiene 5 valores únicos (15, 25, 30, 45, 55) que corresponden exactamente, uno a uno, con los 5 grupos de `Age Group`. Es la misma información repetida en otra forma. | Excluir — redundante con `Age Group`, que sí está documentada. |

## Otros hallazgos de la auditoría

- **Duplicados**: 300 de 3,150 filas (~9.5%) son filas exactamente duplicadas. Los dejo en el dataset por ahora (no hay evidencia de que sean errores de carga y no lo requiere la consigna), pero lo dejo anotado porque puede inflar artificialmente la partición train/test si una fila duplicada cae en ambos lados.
- **Valores ausentes**: cero en las 16 columnas, consistente con lo que declara UCI.
- **Nombres de columna con doble espacio**: `Call  Failure`, `Subscription  Length` y `Charge  Amount` traen dos espacios en vez de uno en el nombre original del CSV — hay que copiarlos tal cual o normalizarlos con `.str.strip()`/regex antes de referenciarlos por nombre, si no da `KeyError`.
