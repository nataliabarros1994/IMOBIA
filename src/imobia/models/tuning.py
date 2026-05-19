"""Hyperparameter tuning com Optuna (busca bayesiana)."""
import optuna
import pandas as pd
from sklearn.model_selection import cross_val_score
from xgboost import XGBRegressor

from imobia.logger import get_logger

log = get_logger(__name__)


def tune_xgboost(
    X: pd.DataFrame,
    y: pd.Series,
    n_trials: int = 30,
    cv: int = 3,
) -> dict:
    """Otimiza hiperparametros do XGBoost com Optuna.

    Args:
        X: features.
        y: target.
        n_trials: numero de tentativas (30 = ~3min, 100 = ~10min).
        cv: numero de folds da cross-validation.

    Returns:
        Dicionario com os melhores hiperparametros encontrados.
    """
    optuna.logging.set_verbosity(optuna.logging.WARNING)

    def objetivo(trial: optuna.Trial) -> float:
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 100, 500, step=50),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
            "reg_alpha": trial.suggest_float("reg_alpha", 1e-3, 10, log=True),
            "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 10, log=True),
            "random_state": 42,
            "n_jobs": -1,
        }
        modelo = XGBRegressor(**params)
        scores = cross_val_score(
            modelo, X, y, cv=cv, scoring="neg_root_mean_squared_error", n_jobs=-1
        )
        return -scores.mean()

    log.info("Iniciando tuning do XGBoost com %d trials", n_trials)
    study = optuna.create_study(direction="minimize")
    study.optimize(objetivo, n_trials=n_trials, show_progress_bar=True)

    log.info("Melhor RMSE: %.2f", study.best_value)
    log.info("Melhores parametros: %s", study.best_params)
    return study.best_params