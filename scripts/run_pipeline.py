"""Pipeline completo: dados -> limpeza -> features -> modelos.

Rode com: python scripts/run_pipeline.py
"""
from imobia.clean.imoveis import pipeline_limpeza
from imobia.collect.dataset import gerar_dataset_sintetico, salvar_dataset
from imobia.features.builder import pipeline_features
from imobia.logger import get_logger
from imobia.models.baseline import treinar_todos

log = get_logger("pipeline")


def main():
    log.info("=" * 60)
    log.info("INICIANDO PIPELINE IMOBIA")
    log.info("=" * 60)

    # 1. Coleta
    df = gerar_dataset_sintetico(5000)
    salvar_dataset(df)

    # 2. Limpeza
    df = pipeline_limpeza(df)

    # 3. Features
    df = pipeline_features(df)

    # 4. Modelagem
    y = df["preco"]
    X = df.drop(columns=["preco", "preco_m2", "categoria_tamanho"])

    resultados = treinar_todos(X, y)

    log.info("=" * 60)
    log.info("RESULTADOS FINAIS")
    log.info("=" * 60)
    for r in resultados:
        log.info("%-20s | MAPE=%5.2f%% | R2=%.3f", r.nome, r.mape, r.r2)


if __name__ == "__main__":
    main()
