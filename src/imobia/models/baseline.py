"""Modelos de regressao para predicao de preco."""
from dataclasses import dataclass

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_percentage_error,
    r2_score,
    root_mean_squared_error,
)
from sklearn.model_selection import cross_val_score, train_test_split

from imobia.logger import get_logger

log = get_logger(__name__)


@dataclass
class ResultadoModelo:
    """Container para metricas de um modelo treinado."""
    nome: str
    rmse: float
    mape: float
    r2: float
    cv_rmse_medio: float
    cv_rmse_std: float


def avaliar_modelo(modelo, X: pd.DataFrame, y: pd.Series, nome: str) -> ResultadoModelo:
    """Treina, avalia e retorna metricas de um modelo.

    Faz split treino/teste 80/20 e cross-validation com 5 folds.
    """
    log.info("Avaliando modelo: %s", nome)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    rmse = root_mean_squared_error(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred) * 100
    r2 = r2_score(y_test, y_pred)

    cv_scores = cross_val_score(
        modelo, X, y, cv=5, scoring="neg_root_mean_squared_error", n_jobs=-1
    )
    cv_rmse = -cv_scores

    resultado = ResultadoModelo(
        nome=nome,
        rmse=rmse,
        mape=mape,
        r2=r2,
        cv_rmse_medio=cv_rmse.mean(),
        cv_rmse_std=cv_rmse.std(),
    )
    log.info(
        "%s: RMSE=%.2f, MAPE=%.2f%%, R2=%.3f",
        nome, resultado.rmse, resultado.mape, resultado.r2,
    )
    return resultado


def treinar_todos(X: pd.DataFrame, y: pd.Series) -> list[ResultadoModelo]:
    """Treina varios modelos e retorna a comparacao."""
    modelos = {
        "Regressao Linear": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
    }
    return [avaliar_modelo(m, X, y, nome) for nome, m in modelos.items()]
