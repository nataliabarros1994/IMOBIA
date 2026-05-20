"""Logger configurado. Use isso em vez de print() no codigo de producao."""
import logging
import sys


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Cria um logger formatado para o projeto.

    Args:
        name: nome do modulo (use __name__).
        level: nivel de log (default INFO).

    Returns:
        Logger configurado.

    Exemplo:
        >>> log = get_logger(__name__)
        >>> log.info("Coletando dados do IBGE")
    """
    logger = logging.getLogger(name)

    # Evita adicionar handlers duplicados se a funcao for chamada varias vezes
    if logger.handlers:
        return logger

    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
