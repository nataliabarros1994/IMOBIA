"""Carrega o dataset de imoveis. Substitua pelo seu dataset real."""
from pathlib import Path

import numpy as np
import pandas as pd

from imobia.logger import get_logger
from imobia.paths import DATA_RAW

log = get_logger(__name__)


def gerar_dataset_sintetico(n: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Gera um dataset sintetico de imoveis para desenvolvimento.

    Util para comecar antes de baixar dados reais. Substitua por scraping
    ou download de dataset real (ex.: Kaggle 'brazilian-houses-to-rent').

    Args:
        n: numero de imoveis.
        seed: semente para reproducibilidade.

    Returns:
        DataFrame com colunas tipicas de anuncio imobiliario.
    """
    log.info("Gerando dataset sintetico com %d imoveis", n)
    rng = np.random.default_rng(seed)

    bairros = [
        "Copacabana", "Ipanema", "Leblon", "Botafogo", "Tijuca",
        "Barra da Tijuca", "Recreio", "Jacarepagua", "Meier", "Centro",
        "Flamengo", "Laranjeiras", "Vila Isabel", "Grajau", "Santa Teresa",
    ]
    preco_base = {
        "Copacabana": 12000, "Ipanema": 18000, "Leblon": 22000,
        "Botafogo": 11000, "Tijuca": 7500, "Barra da Tijuca": 13000,
        "Recreio": 8500, "Jacarepagua": 6000, "Meier": 5500, "Centro": 6000,
        "Flamengo": 10000, "Laranjeiras": 9500, "Vila Isabel": 6500,
        "Grajau": 7000, "Santa Teresa": 8000,
    }

    bairro = rng.choice(bairros, size=n)
    area = rng.integers(25, 350, size=n)
    quartos = rng.integers(1, 6, size=n)
    banheiros = np.clip(quartos + rng.integers(0, 3, size=n), 1, 6)
    vagas = rng.integers(0, 4, size=n)
    andar = rng.integers(0, 25, size=n)
    idade = rng.integers(0, 60, size=n)

    preco_m2 = np.array([preco_base[b] for b in bairro])
    fator_idade = 1 - (idade / 200)
    fator_andar = 1 + (andar / 200)
    ruido = rng.normal(1, 0.15, size=n)
    preco = area * preco_m2 * fator_idade * fator_andar * ruido

    df = pd.DataFrame(
        {
            "bairro": bairro,
            "area_m2": area,
            "quartos": quartos,
            "banheiros": banheiros,
            "vagas": vagas,
            "andar": andar,
            "idade_anos": idade.astype(float),
            "preco": preco.round(2),
        }
    )

    faltantes_idx = rng.choice(n, size=n // 20, replace=False)
    df.loc[faltantes_idx, "idade_anos"] = np.nan

    return df


def salvar_dataset(df: pd.DataFrame, nome: str = "imoveis.csv") -> Path:
    """Salva o dataset em data/raw/."""
    caminho = DATA_RAW / nome
    df.to_csv(caminho, index=False)
    log.info("Dataset salvo em %s (%d linhas)", caminho, len(df))
    return caminho


if __name__ == "__main__":
    df = gerar_dataset_sintetico()
    salvar_dataset(df)
    print(df.head())
    print(f"\nFormato: {df.shape}")
    print(f"\nTipos:\n{df.dtypes}")
