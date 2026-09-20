import pandas as pd

TARGET = "Churn"
REQUIRED = {TARGET, "Complains"}


def load_data():
    return pd.read_csv("data/raw/dataset.csv")


def test_dataset_is_not_empty():
    assert not load_data().empty


def test_required_columns_exist():
    assert REQUIRED <= set(load_data().columns)


def test_target_has_no_missing_and_two_classes():
    y = load_data()[TARGET]
    assert y.notna().all()
    assert y.nunique() >= 2


def test_known_undocumented_column_still_present():
    # "Age" viene en el archivo oficial de UCI pero no está en su tabla de
    # variables documentada (ver docs/diccionario_datos.md): duplica
    # "Age Group" 1 a 1. La excluyo a mano en el notebook (DROP_COLUMNS).
    # Si esta prueba falla, es porque la fuente cambió su esquema y hay que
    # revisar de nuevo qué columnas retirar antes de reentrenar.
    columns = set(load_data().columns)
    known_undocumented = {"Age"}
    assert known_undocumented <= columns
