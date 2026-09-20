"""Utilidades de "Green AI" para el LAB03: frontera de Pareto entre
desempeño (F1 macro) y costo (tiempo mediano de ajuste).

Vive en su propio módulo -- no solo en el notebook -- porque
`tests/test_green.py` la importa directamente (`from inf8239_u01.green
import pareto_flags`), y porque la misma lógica se reutiliza tanto en el
notebook como en cualquier script de reporting futuro sin copiar/pegar
código.
"""

import pandas as pd


def pareto_flags(df: pd.DataFrame, score: str = "f1_macro", cost: str = "fit_median_s") -> list:
    """Marca qué filas de `df` son óptimas de Pareto entre `score` (a
    maximizar) y `cost` (a minimizar).

    Una fila está dominada si existe OTRA fila que es al menos igual de
    buena en ambas columnas y estrictamente mejor en al menos una (más
    `score` o menos `cost`). Devuelve `True` para las filas NO dominadas
    (las que sí conviene considerar) y `False` para las dominadas (hay
    otra opción que es igual o mejor en todo).

    Uso más simple con pandas puro (sin numpy vectorizado) a propósito:
    el dataset de modelos es de a lo sumo unas pocas decenas de filas, así
    que un doble recorrido O(n^2) es perfectamente legible y suficiente.
    """
    flags = []
    for _, row in df.iterrows():
        dominated = (
            (df[score] >= row[score])
            & (df[cost] <= row[cost])
            & ((df[score] > row[score]) | (df[cost] < row[cost]))
        ).any()
        flags.append(not bool(dominated))
    return flags
