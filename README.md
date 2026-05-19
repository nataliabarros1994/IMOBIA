# ImobIA

Análise e previsão de preços do mercado imobiliário brasileiro com IA generativa.

## Setup

```bash
conda create -n imobia python=3.13.9 -y
conda activate imobia
pip install -e ".[dev]"
```

## Estrutura

- `src/imobia/` — código-fonte
- `notebooks/` — análises exploratórias
- `data/` — dados (não versionados)
- `tests/` — testes
- `docs/` — documentação

## Roadmap

- [ ] Fase 1 — Definição do problema de negócio
- [ ] Fase 2 — Coleta de dados (scraping + IBGE)
- [ ] Fase 3 — Banco de dados (Postgres + MongoDB)
- [ ] Fase 4 — Limpeza e EDA
- [ ] Fase 5 — Modelos supervisionados
- [ ] Fase 6 — Modelos não-supervisionados
- [ ] Fase 7 — IA generativa
- [ ] Fase 8 — Dashboard e documentação final
