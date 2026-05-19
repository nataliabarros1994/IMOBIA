# Fase 1 — Definicao do Problema

## Cidade alvo
Rio de Janeiro (RJ) — Capital e regiao metropolitana.

## Perguntas de negocio

1. **Predicao de preco**: dado um conjunto de caracteristicas de um imovel
   (area, quartos, banheiros, vagas, bairro), conseguimos estimar seu preco
   de venda com erro medio menor que 15%?

2. **Bairros subvalorizados**: quais bairros tem preco/m2 abaixo do esperado
   considerando indicadores socioeconomicos (renda, IDH, infraestrutura)?

3. **Segmentacao**: existem agrupamentos naturais de imoveis no Rio que
   permitem criar "personas" de mercado (ex.: studio jovem, familia classe
   media, alto padrao)?

## Stakeholders ficticios
- Imobiliarias: querem precificar imoveis com mais precisao.
- Investidores: querem identificar bairros com potencial de valorizacao.
- Compradores: querem saber se o preco de um imovel esta justo.

## Metricas de sucesso
- Modelo de regressao com MAPE < 15% no conjunto de teste.
- Identificacao de pelo menos 3 clusters de imoveis interpretaveis.
- Dashboard com insights acionaveis para os stakeholders.

## Premissas e limitacoes
- Dados de anuncios refletem preco pedido, nao preco fechado.
- Periodo de analise: 2024-2026 (dados mais recentes disponiveis).
- Nao consideramos variaveis macroeconomicas (juros, inflacao).
