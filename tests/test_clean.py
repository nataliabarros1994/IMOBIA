"""Testes da limpeza de dados."""
import numpy as np
import pandas as pd
import pytest

from imobia.clean.imoveis import imputar_faltantes, remover_duplicatas, remover_outliers_iqr


@pytest.fixture
def df_exemplo():
    return pd.DataFrame({
        "preco": [100.0, 200.0, 300.0, 400.0, 500.0, 100000.0],  # ultimo eh outlier
        "area_m2": [50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
        "quartos": [1.0, 2.0, np.nan, 3.0, 2.0, 4.0],
    })


def test_remover_duplicatas():
    df = pd.DataFrame({"a": [1, 1, 2], "b": [1, 1, 2]})
    assert len(remover_duplicatas(df)) == 2


def test_remover_outliers_iqr(df_exemplo):
    resultado = remover_outliers_iqr(df_exemplo, "preco")
    assert 100000.0 not in resultado["preco"].values


def test_imputar_faltantes(df_exemplo):
    resultado = imputar_faltantes(df_exemplo)
    assert not resultado.isna().any().any()
