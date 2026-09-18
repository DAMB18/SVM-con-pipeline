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


def test_known_undocumented_columns_still_present():
    # FN, FP y Age no están documentadas por UCI (ver docs/diccionario_datos.md):
    # FN duplica Customer Value, FP no tiene definición confiable, y Age
    # duplica Age Group. Las excluyo a mano en el notebook (DROP_COLUMNS).
    # Si esta prueba falla, es porque la fuente cambió su esquema y hay que
    # revisar de nuevo qué columnas retirar antes de reentrenar.
    columns = set(load_data().columns)
    known_undocumented = {"FN", "FP", "Age"}
    assert known_undocumented <= columns
