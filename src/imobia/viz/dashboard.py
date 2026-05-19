"""Dashboard interativo do ImobIA.

Para rodar:
    streamlit run src/imobia/viz/dashboard.py
"""
import pandas as pd
import streamlit as st

from imobia.paths import DATA_RAW
from imobia.viz.plots import boxplot_por_bairro, histograma_precos

st.set_page_config(page_title="ImobIA", page_icon="🏠", layout="wide")
st.title("🏠 ImobIA — Analise do mercado imobiliario do Rio")


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    return pd.read_csv(DATA_RAW / "imoveis.csv")


df = carregar_dados()

# Sidebar com filtros
st.sidebar.header("Filtros")
bairros = st.sidebar.multiselect("Bairros", sorted(df["bairro"].unique()))
faixa_preco = st.sidebar.slider(
    "Faixa de preco (R$ mil)",
    int(df["preco"].min() / 1000),
    int(df["preco"].max() / 1000),
    (200, 2000),
)

df_filt = df[
    (df["preco"] >= faixa_preco[0] * 1000) & (df["preco"] <= faixa_preco[1] * 1000)
]
if bairros:
    df_filt = df_filt[df_filt["bairro"].isin(bairros)]

# Metricas
col1, col2, col3, col4 = st.columns(4)
col1.metric("Imoveis", f"{len(df_filt):,}")
col2.metric("Preco medio", f"R$ {df_filt['preco'].mean()/1000:,.0f}k")
col3.metric("Area media", f"{df_filt['area_m2'].mean():.0f} m²")
col4.metric("Preco/m2 medio", f"R$ {(df_filt['preco']/df_filt['area_m2']).mean():,.0f}")

# Graficos
st.subheader("Distribuicao de precos")
st.pyplot(histograma_precos(df_filt))

st.subheader("Preco/m2 por bairro")
st.pyplot(boxplot_por_bairro(df_filt))

st.subheader("Amostra dos dados")
st.dataframe(df_filt.sample(min(100, len(df_filt))))