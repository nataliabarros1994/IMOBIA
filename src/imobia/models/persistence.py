"""Persistencia de modelos treinados (salvar e carregar)."""
from pathlib import Path
from typing import Any

import joblib

from imobia.logger import get_logger
from imobia.paths import MODELS

log = get_logger(__name__)


def salvar_modelo(modelo: Any, nome: str, versao: str = "v1") -> Path:
    """Salva um modelo treinado em disco.

    Args:
        modelo: objeto do modelo (sklearn, xgboost, etc).
        nome: nome do modelo (ex: 'xgboost_precos').
        versao: versao (ex: 'v1', 'v2').

    Returns:
        Caminho do arquivo salvo.
    """
    caminho = MODELS / f"{nome}_{versao}.joblib"
    joblib.dump(modelo, caminho)
    log.info("Modelo salvo: %s (%.1f KB)", caminho, caminho.stat().st_size / 1024)
    return caminho


def carregar_modelo(nome: str, versao: str = "v1") -> Any:
    """Carrega um modelo previamente salvo.

    Args:
        nome: nome do modelo.
        versao: versao desejada.

    Returns:
        Objeto do modelo carregado.
    """
    caminho = MODELS / f"{nome}_{versao}.joblib"
    if not caminho.exists():
        raise FileNotFoundError(f"Modelo nao encontrado: {caminho}")
    log.info("Carregando modelo de %s", caminho)
    return joblib.load(caminho)


def listar_modelos() -> list[str]:
    """Lista todos os modelos salvos."""
    return [p.stem for p in MODELS.glob("*.joblib")]