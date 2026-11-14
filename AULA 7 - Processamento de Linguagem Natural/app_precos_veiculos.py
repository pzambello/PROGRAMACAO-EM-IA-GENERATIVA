"""
Avaliador de Preços de Veículos Usados - Streamlit + TensorFlow + Tabela FIPE
Arquivo único: busca marca/modelo/ano na API pública da FIPE, obtém o preço de
tabela e ajusta o valor conforme a quilometragem (referência: 10.000 km/ano).
"""

import datetime
import re

import numpy as np
import pandas as pd
import requests
import streamlit as st
import tensorflow as tf

# ---------------------------------------------------------------------------
# 1) CONFIGURAÇÕES GERAIS
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Avaliador de Veículos", page_icon="🚗", layout="centered")

API_FIPE = "https://fipe.parallelum.com.br/api/v2/cars"  # API pública (gratuita)
KM_IDEAL_POR_ANO = 12_000  # quilometragem "neutra": não altera o preço da tabela
ANO_ATUAL = datetime.date.today().year


# ---------------------------------------------------------------------------
# 2) CONSULTAS À API DA FIPE
# @st.cache_data guarda as respostas por 24 h: evita chamadas repetidas
# (a API gratuita tem limite diário de requisições) e deixa o app mais rápido.
# ---------------------------------------------------------------------------
@st.cache_data(ttl=86_400, show_spinner=False)
def consultar_fipe(caminho: str):
    """Faz um GET na API e devolve o JSON. Lança exceção em caso de erro."""
    resposta = requests.get(f"{API_FIPE}{caminho}", timeout=20)
    resposta.raise_for_status()  # transforma erro HTTP (404, 429...) em exceção
    return resposta.json()


def como_lista(dados) -> list:
    """Padroniza a resposta: a API devolve lista de {code, name}."""
    if isinstance(dados, dict):  # tolera formato antigo da API (v1)
        dados = dados.get("modelos", [])
    return dados


def preco_para_float(texto: str) -> float:
    """Converte 'R$ 52.340,00' em 52340.0."""
    limpo = re.sub(r"[^\d,]", "", texto).replace(",", ".")
    return float(limpo)


def ano_do_codigo(codigo_ano: str) -> int:
    """'2015-1' -> 2015. O código 32000 representa veículo zero km."""
    ano = int(codigo_ano.split("-")[0])
    return ANO_ATUAL if ano == 32000 else ano


# ---------------------------------------------------------------------------
# 3) MODELO DE REGRESSÃO LINEAR COM TENSORFLOW
# Relação aprendida:  razão de preço = a * (diferença de km) + b
#   - diferença de km = (km real - km ideal) / 10.000   (positivo = rodou demais)
#   - razão de preço  = preço de venda / preço FIPE      (1,0 = igual à tabela)
# Não existe base pública de anúncios nesta aplicação; por isso o modelo aprende
# a partir de dados sintéticos gerados com a regra de negócio da empresa
# (parâmetro "taxa", ajustável na barra lateral). Troque por dados reais quando
# houver histórico de vendas.
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="Treinando o modelo de regressão...")
def treinar_regressao(taxa_por_10mil_km: float):
    tf.keras.utils.set_random_seed(42)  # resultados reproduzíveis

    # Dados sintéticos: de -10 (rodou muito menos) a +30 (rodou muito mais)
    x = np.random.uniform(-10, 30, size=(3000, 1)).astype("float32")
    ruido = np.random.normal(0, 0.005, size=(3000, 1)).astype("float32")
    y = 1.0 - taxa_por_10mil_km * x + ruido

    # Regressão linear simples = uma única camada Dense com 1 neurônio
    modelo = tf.keras.Sequential([tf.keras.Input(shape=(1,)), tf.keras.layers.Dense(1)])
    modelo.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.05), loss="mse")
    modelo.fit(x, y, epochs=60, batch_size=64, verbose=0)
    return modelo


def estimar_preco(modelo, preco_fipe: float, km: np.ndarray, ano_modelo: int) -> np.ndarray:
    """Devolve o preço estimado para cada quilometragem informada."""
    idade = max(ANO_ATUAL - ano_modelo, 1)  # mínimo de 1 ano de referência
    km_ideal = KM_IDEAL_POR_ANO * idade
    diferenca = ((km - km_ideal) / 12_000).reshape(-1, 1).astype("float32")
    razao = modelo.predict(diferenca, verbose=0).flatten()
    razao = np.clip(razao, 0.50, 1.25)  # limites de segurança: -50% a +25%
    return preco_fipe * razao


# ---------------------------------------------------------------------------
# 4) BARRA LATERAL
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Parâmetros")
    taxa_pct = st.slider(
        "Variação de preço a cada 12.000 km de diferença (%)",
        min_value=0.5, max_value=3.0, value=1.5, step=0.1,
        help="Quanto o preço sobe/desce a cada 12.000 km abaixo/acima da quilometragem ideal.",
    )
    st.caption("Quilometragem ideal: 12.000 km × idade do veículo (mín. 1 ano).")

modelo_tf = treinar_regressao(taxa_pct / 100)

# ---------------------------------------------------------------------------
# 5) INTERFACE: SELEÇÃO DE MARCA, MODELO E ANO (dados da FIPE)
# ---------------------------------------------------------------------------
st.title("🚗 Avaliador de Veículos Usados")
st.write("Selecione o veículo e informe a quilometragem para estimar o valor de mercado.")

try:
    marcas = como_lista(consultar_fipe("/brands"))
    marca = st.selectbox("Marca", marcas, format_func=lambda m: m["name"], index=None,
                         placeholder="Escolha a marca")
    if marca is None:
        st.stop()  # interrompe a execução até o usuário escolher

    modelos = como_lista(consultar_fipe(f"/brands/{marca['code']}/models"))
    modelo = st.selectbox("Modelo", modelos, format_func=lambda m: m["name"], index=None,
                          placeholder="Escolha o modelo")
    if modelo is None:
        st.stop()

    anos = como_lista(consultar_fipe(f"/brands/{marca['code']}/models/{modelo['code']}/years"))
    ano = st.selectbox("Ano / combustível", anos, format_func=lambda a: a["name"], index=None,
                       placeholder="Escolha o ano")
    if ano is None:
        st.stop()

    ficha = consultar_fipe(
        f"/brands/{marca['code']}/models/{modelo['code']}/years/{ano['code']}"
    )
except requests.RequestException as erro:
    st.error(f"Não foi possível consultar a tabela FIPE agora. Tente novamente em instantes. ({erro})")
    st.stop()

preco_fipe = preco_para_float(ficha["price"])
ano_modelo = ano_do_codigo(ano["code"])
idade = max(ANO_ATUAL - ano_modelo, 1)
km_ideal = KM_IDEAL_POR_ANO * idade

st.divider()
st.subheader(f"{ficha.get('brand', marca['name'])} {ficha.get('model', modelo['name'])}")
st.caption(
    f"Código FIPE: {ficha.get('codeFipe', '-')} · Referência: {ficha.get('referenceMonth', '-')} · "
    f"Combustível: {ficha.get('fuel', '-')}"
)

# ---------------------------------------------------------------------------
# 6) QUILOMETRAGEM E RESULTADO
# ---------------------------------------------------------------------------
km = st.slider("Quilometragem do veículo (km)", 0, 500_000, min(km_ideal, 500_000), step=1_000)

preco_estimado = float(estimar_preco(modelo_tf, preco_fipe, np.array([km]), ano_modelo)[0])
variacao = preco_estimado / preco_fipe - 1


def brl(valor: float) -> str:
    """Formata em reais no padrão brasileiro (R$ 1.234,56)."""
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


col1, col2, col3 = st.columns(3)
col1.metric("Preço FIPE", brl(preco_fipe))
col2.metric("Preço estimado", brl(preco_estimado), f"{variacao:+.1%} vs. FIPE")
col3.metric("Km ideal", f"{km_ideal:,.0f} km".replace(",", "."))

if km > km_ideal:
    st.info(f"Quilometragem **acima** do ideal em {km - km_ideal:,.0f} km: valor reduzido.".replace(",", "."))
elif km < km_ideal:
    st.info(f"Quilometragem **abaixo** do ideal em {km_ideal - km:,.0f} km: valor valorizado.".replace(",", "."))
else:
    st.info("Quilometragem exatamente no ideal: valor igual ao da tabela.")

# Gráfico: como o preço varia ao longo de toda a faixa de quilometragem
faixa_km = np.arange(0, 300_001, 5_000)
grafico = pd.DataFrame(
    {"Preço estimado (R$)": estimar_preco(modelo_tf, preco_fipe, faixa_km, ano_modelo)},
    index=pd.Index(faixa_km, name="Quilometragem (km)"),
)
st.line_chart(grafico)
st.caption(
    "Estimativa de apoio à negociação, baseada na tabela FIPE e em regra de depreciação por "
    "quilometragem. Não considera estado de conservação, opcionais ou condições de mercado locais."
)
