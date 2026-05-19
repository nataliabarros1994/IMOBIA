"""Caminhos do projeto. Centralizar aqui evita strings hardcoded espalhadas."""
from pathlib import Path


# Path(__file__) eh o caminho desse proprio arquivo paths.py
# .resolve() converte pra caminho absoluto
# .parents[2] sobe 2 niveis: src/imobia -> src -> ImobIA (raiz)
ROOT = Path(__file__).resolve().parents[2]

DATA = ROOT / "data"
DATA_RAW = DATA / "raw"
DATA_INTERIM = DATA / "interim"
DATA_PROCESSED = DATA / "processed"
DATA_EXTERNAL = DATA / "external"

NOTEBOOKS = ROOT / "notebooks"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
MODELS = ROOT / "models"

# Cria as pastas se nao existirem. exist_ok=True evita erro se ja existe.
for p in (DATA_RAW, DATA_INTERIM, DATA_PROCESSED, DATA_EXTERNAL, FIGURES, MODELS):
    p.mkdir(parents=True, exist_ok=True)