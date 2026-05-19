"""Modelos de clustering para segmentar imoveis."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from imobia.logger import get_logger

log = get_logger(__name__)


def encontrar_k_otimo(X: pd.DataFrame, k_max: int = 10) -> dict[int, float]:
    """Calcula inercia para varios k (metodo do cotovelo)."""
    X_scaled = StandardScaler().fit_transform(X)
    inercias = {}
    for k in range(2, k_max + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inercias[k] = km.inertia_
        log.info("k=%d: inercia=%.2f", k, km.inertia_)
    return inercias


def segmentar_imoveis(X: pd.DataFrame, k: int = 4) -> tuple[np.ndarray, pd.DataFrame]:
    """Aplica KMeans + PCA. Retorna labels e DataFrame 2D para plot."""
    log.info("Segmentando imoveis em %d clusters", k)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    X_2d = pca.fit_transform(X_scaled)
    df_plot = pd.DataFrame(X_2d, columns=["pc1", "pc2"])
    df_plot["cluster"] = labels

    log.info("Variancia explicada (PC1+PC2): %.2f%%", pca.explained_variance_ratio_.sum() * 100)
    return labels, df_plot