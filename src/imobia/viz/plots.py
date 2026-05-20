"""Funcoes de visualizacao reutilizaveis."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

sns.set_theme(style="whitegrid", palette="muted")


def histograma_precos(df: pd.DataFrame, bins: int = 50) -> Figure:
    """Histograma da distribuicao de precos."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df["preco"] / 1000, bins=bins, edgecolor="black", alpha=0.7)
    ax.set_xlabel("Preco (R$ mil)")
    ax.set_ylabel("Frequencia")
    ax.set_title("Distribuicao de precos dos imoveis")
    fig.tight_layout()
    return fig


def boxplot_por_bairro(df: pd.DataFrame, top_n: int = 10) -> Figure:
    """Boxplot de preco/m2 dos top N bairros mais frequentes."""
    df = df.copy()
    df["preco_m2"] = df["preco"] / df["area_m2"]
    top_bairros = df["bairro"].value_counts().head(top_n).index
    df_top = df[df["bairro"].isin(top_bairros)]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df_top, x="bairro", y="preco_m2", ax=ax, order=list(top_bairros))
    ax.set_xlabel("Bairro")
    ax.set_ylabel("Preco por m2 (R$)")
    ax.set_title(f"Preco/m2 nos {top_n} bairros mais frequentes")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    return fig


def matriz_correlacao(df: pd.DataFrame) -> Figure:
    """Heatmap das correlacoes entre variaveis numericas."""
    numericas = df.select_dtypes(include="number")
    corr = numericas.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Matriz de correlacao")
    fig.tight_layout()
    return fig
