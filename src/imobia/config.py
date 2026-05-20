"""Configuracoes do projeto carregadas do arquivo .env."""
import os
from dataclasses import dataclass

from dotenv import load_dotenv

from imobia.paths import ROOT

# Le o arquivo .env e injeta as variaveis no os.environ
load_dotenv(ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    """Configuracoes imutaveis acessadas em todo o projeto.

    frozen=True torna a dataclass imutavel (nao pode mudar valor depois).
    """

    # API do Claude
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    # PostgreSQL
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db: str = os.getenv("POSTGRES_DB", "imobia")
    postgres_user: str = os.getenv("POSTGRES_USER", "imobia")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "")

    # MongoDB
    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/imobia")

    @property
    def postgres_url(self) -> str:
        """URL completa pro SQLAlchemy conectar no Postgres."""
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


# Instancia unica que voce importa em outros modulos:
#   from imobia.config import settings
settings = Settings()
