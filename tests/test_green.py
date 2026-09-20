import pandas as pd

from inf8239_u01.green import pareto_flags


def test_pareto_marks_dominated_rows():
    df = pd.DataFrame({"f1_macro": [.90, .90, .88], "fit_median_s": [2., 1., 3.]})
    assert pareto_flags(df) == [False, True, False]


def test_single_model_is_pareto():
    df = pd.DataFrame({"f1_macro": [.8], "fit_median_s": [1.]})
    assert pareto_flags(df) == [True]


def test_faster_and_better_model_dominates():
    # Un modelo que es al mismo tiempo más rápido y con mejor F1 que otro
    # debe dejar a ese otro fuera de la frontera.
    df = pd.DataFrame({
        "model": ["lento_peor", "rapido_mejor"],
        "f1_macro": [.70, .95],
        "fit_median_s": [5.0, 0.5],
    })
    assert pareto_flags(df) == [False, True]


def test_equal_rows_are_not_dominated():
    # Ninguna fila domina a otra si son idénticas en ambas columnas.
    df = pd.DataFrame({"f1_macro": [.85, .85], "fit_median_s": [1.0, 1.0]})
    assert pareto_flags(df) == [True, True]
