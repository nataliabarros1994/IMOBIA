"""Enriquece o dataset de imoveis com dados socioeconomicos do IBGE.

Adiciona indicadores de bairro (renda, IDH, populacao) ao dataset principal,
util para modelos que precisam contexto socioeconomico.
"""
import pandas as pd

from imobia.logger import get_logger

log = get_logger(__name__)


# Dados ficticios para enriquecimento. Em producao, viria do IBGE.
INDICADORES_BAIRROS_RJ = {
    "Copacabana":       {"zona": "Sul",    "idh": 0.937, "renda_media": 5500, "populacao": 146392},
    "Ipanema":          {"zona": "Sul",    "idh": 0.961, "renda_media": 7800, "populacao": 41136},
    "Leblon":           {"zona": "Sul",    "idh": 0.967, "renda_media": 9200, "populacao": 23420},
    "Botafogo":         {"zona": "Sul",    "idh": 0.929, "renda_media": 5100, "populacao": 82890},
    "Tijuca":           {"zona": "Norte",  "idh": 0.913, "renda_media": 3800, "populacao": 163805},
    "Barra da Tijuca":  {"zona": "Oeste",  "idh": 0.951, "renda_media": 6800, "populacao": 135924},
    "Recreio":          {"zona": "Oeste",  "idh": 0.923, "renda_media": 4200, "populacao": 82240},
    "Jacarepagua":      {"zona": "Oeste",  "idh": 0.871, "renda_media": 2800, "populacao": 157326},
    "Meier":            {"zona": "Norte",  "idh": 0.886, "renda_media": 2500, "populacao": 49828},
    "Centro":           {"zona": "Centro", "idh": 0.890, "renda_media": 3200, "populacao": 41142},
    "Flamengo":         {"zona": "Sul",    "idh": 0.928, "renda_media": 5600, "populacao": 58271},
    "Laranjeiras":      {"zona": "Sul",    "idh": 0.937, "renda_media": 6100, "populacao": 39200},
    "Vila Isabel":      {"zona": "Norte",  "idh": 0.901, "renda_media": 3200, "populacao": 87187},
    "Grajau":           {"zona": "Norte",  "idh": 0.907, "renda_media": 3400, "populacao": 38432},
    "Santa Teresa":     {"zona": "Centro", "idh": 0.882, "renda_media": 2900, "populacao": 40923},
}


def enriquecer_imoveis(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona colunas socioeconomicas baseado no bairro.

    Args:
        df: DataFrame com coluna 'bairro'.

    Returns:
        DataFrame original + zona, idh, renda_media, populacao.
    """
    log.info("Enriquecendo %d imoveis com dados de bairro", len(df))

    indicadores = pd.DataFrame.from_dict(INDICADORES_BAIRROS_RJ, orient="index")
    indicadores.index.name = "bairro"
    indicadores = indicadores.reset_index()

    df_enriquecido = df.merge(indicadores, on="bairro", how="left")

    # Imputa medias para bairros nao mapeados
    cols_numericas = ["idh", "renda_media", "populacao"]
    for col in cols_numericas:
        if df_enriquecido[col].isna().any():
            valor = df_enriquecido[col].median()
            df_enriquecido[col] = df_enriquecido[col].fillna(valor)
            log.info("Imputados faltantes em '%s' com mediana = %.2f", col, valor)

    df_enriquecido["zona"] = df_enriquecido["zona"].fillna("Outras")

    log.info("Dataset enriquecido: %d linhas, %d colunas", *df_enriquecido.shape)
    return df_enriquecido
