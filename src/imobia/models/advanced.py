"""Modelos avancados de gradient boosting (XGBoost e LightGBM)."""
import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.metrics import (
    mean_absolute_percentage_error,
    r2_score,
    root_mean_squared_error,
)
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

from imobia.logger import get_logger
from imobia.models.baseline import ResultadoModelo

log = get_logger(__name__)


def treinar_xgboost(
    X: pd.DataFrame, y: pd.Series, params: dict | None = None
) -> tuple[ResultadoModelo, XGBRegressor]:
    """Treina XGBoost com parametros padrao ou customizados.

    Args:
        X: features.
        y: target (preco).
        params: hiperparametros customizados (opcional).

    Returns:
        Tupla (ResultadoModelo, modelo treinado).
    """
    params_padrao = {
        "n_estimators": 300,
        "max_depth": 6,
        "learning_rate": 0.05,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "random_state": 42,
        "n_jobs": -1,
    }
    if params:
        params_padrao.update(params)

    log.info("Treinando XGBoost com %s", params_padrao)
    modelo = XGBRegressor(**params_padrao)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    resultado = ResultadoModelo(
        nome="XGBoost",
        rmse=root_mean_squared_error(y_test, y_pred),
        mape=mean_absolute_percentage_error(y_test, y_pred) * 100,
        r2=r2_score(y_test, y_pred),
        cv_rmse_medio=0.0,
        cv_rmse_std=0.0,
    )
    log.info(
        "XGBoost: RMSE=%.2f, MAPE=%.2f%%, R2=%.3f",
        resultado.rmse, resultado.mape, resultado.r2,
    )
    return resultado, modelo


def treinar_lightgbm(
    X: pd.DataFrame, y: pd.Series, params: dict | None = None
) -> tuple[ResultadoModelo, LGBMRegressor]:
    """Treina LightGBM (geralmente mais rapido que XGBoost)."""
    params_padrao = {
        "n_estimators": 300,
        "max_depth": 6,
        "learning_rate": 0.05,
        "num_leaves": 31,
        "random_state": 42,
        "n_jobs": -1,
        "verbose": -1,
    }
    if params:
        params_padrao.update(params)

    log.info("Treinando LightGBM")
    modelo = LGBMRegressor(**params_padrao)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    modelo.fit(X_train, y_train)
    # np.asarray() resolve o tipo amplo do LGBMRegressor.predict()
    y_pred = np.asarray(modelo.predict(X_test))

    resultado = ResultadoModelo(
        nome="LightGBM",
        rmse=root_mean_squared_error(y_test, y_pred),
        mape=mean_absolute_percentage_error(y_test, y_pred) * 100,
        r2=r2_score(y_test, y_pred),
        cv_rmse_medio=0.0,
        cv_rmse_std=0.0,
    )
    log.info(
        "LightGBM: RMSE=%.2f, MAPE=%.2f%%, R2=%.3f",
        resultado.rmse, resultado.mape, resultado.r2,
    )
    return resultado, modelo


def importancia_features(modelo, feature_names: list[str], top_n: int = 15) -> pd.DataFrame:
    """Extrai importancia das features (funciona com XGBoost, LightGBM, RandomForest)."""
    if hasattr(modelo, "feature_importances_"):
        importancias = modelo.feature_importances_
    else:
        raise ValueError("Modelo nao possui feature_importances_")

    df = pd.DataFrame({
        "feature": feature_names,
        "importancia": importancias,
    })
    return df.sort_values("importancia", ascending=False).head(top_n)