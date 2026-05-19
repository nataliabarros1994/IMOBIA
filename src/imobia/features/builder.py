"""Construcao de features derivadas para os modelos."""
import pandas as pd

from imobia.logger import get_logger

log = get_logger(__name__)


def adicionar_preco_m2(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula preco por metro quadrado."""
    df = df.copy()
    df["preco_m2"] = df["preco"] / df["area_m2"]
    return df


def codificar_bairros(df: pd.DataFrame, coluna: str = "bairro") -> pd.DataFrame:
    """One-hot encoding para a coluna de bairros."""
    return pd.get_dummies(df, columns=[coluna], prefix="bairro", drop_first=True)


def adicionar_categoria_tamanho(df: pd.DataFrame) -> pd.DataFrame:
    """Cria categoria de tamanho baseada em area."""
    df = df.copy()
    df["categoria_tamanho"] = pd.cut(
        df["area_m2"],
        bins=[0, 50, 100, 200, float("inf")],
        labels=["compacto", "medio", "grande", "muito_grande"],
    )
    return df


def pipeline_features(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica todo o pipeline de feature engineering."""
    log.info("Construindo features")
    df = adicionar_preco_m2(df)
    df = adicionar_categoria_tamanho(df)
    df = codificar_bairros(df)
    return df