"""Funcoes de limpeza para os dados de imoveis."""
import numpy as np
import pandas as pd

from imobia.logger import get_logger

log = get_logger(__name__)


def remover_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas duplicadas."""
    antes = len(df)
    df = df.drop_duplicates()
    log.info("Removidas %d duplicatas", antes - len(df))
    return df


def remover_outliers_iqr(df: pd.DataFrame, coluna: str, k: float = 1.5) -> pd.DataFrame:
    """Remove outliers usando regra do intervalo interquartil (IQR).

    Args:
        df: DataFrame.
        coluna: coluna numerica para filtrar.
        k: multiplicador (1.5 = padrao, 3 = mais permissivo).
    """
    q1, q3 = df[coluna].quantile([0.25, 0.75])
    iqr = q3 - q1
    limite_inf = q1 - k * iqr
    limite_sup = q3 + k * iqr
    antes = len(df)
    df = df[(df[coluna] >= limite_inf) & (df[coluna] <= limite_sup)]
    log.info(
        "Removidos %d outliers em '%s' (limites: %.2f a %.2f)",
        antes - len(df), coluna, limite_inf, limite_sup,
    )
    return df


def imputar_faltantes(df: pd.DataFrame, estrategia: str = "mediana") -> pd.DataFrame:
    """Preenche valores faltantes em colunas numericas."""
    numericas = df.select_dtypes(include=np.number).columns
    for col in numericas:
        if df[col].isna().any():
            if estrategia == "mediana":
                valor = df[col].median()
            elif estrategia == "media":
                valor = df[col].mean()
            else:
                raise ValueError(f"Estrategia '{estrategia}' nao suportada")
            df[col] = df[col].fillna(valor)
            log.info("Imputados faltantes em '%s' com %s = %.2f", col, estrategia, valor)
    return df


def pipeline_limpeza(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica todas as etapas de limpeza em sequencia."""
    log.info("Iniciando pipeline de limpeza (%d linhas)", len(df))
    df = remover_duplicatas(df)
    df = remover_outliers_iqr(df, "preco")
    df = remover_outliers_iqr(df, "area_m2")
    df = imputar_faltantes(df)
    log.info("Pipeline finalizado (%d linhas)", len(df))
    return df
