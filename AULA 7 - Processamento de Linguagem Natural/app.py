"""
Detector de Spam em E-mails - Streamlit + TensorFlow
Arquivo único: treina um classificador de texto simples e exibe a interface web.
"""

import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf

# ---------------------------------------------------------------------------
# 1) CONFIGURAÇÃO DA PÁGINA
# Deve ser o primeiro comando Streamlit do script.
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Detector de Spam", page_icon="📧", layout="centered")

# ---------------------------------------------------------------------------
# 2) DADOS DE TREINO INICIAIS
# Conjunto pequeno, apenas para a aplicação funcionar de imediato.
# Para uso real, envie um CSV maior pela barra lateral (colunas: texto, rotulo).
# rotulo: 1 = spam, 0 = não spam
# ---------------------------------------------------------------------------
SPAM = [
    "Parabéns! Você ganhou um prêmio de R$ 10.000. Clique aqui para resgatar agora",
    "Oferta imperdível: compre 1 leve 3, só hoje, clique no link",
    "Seu empréstimo foi pré-aprovado sem consulta ao SPC, responda já",
    "Ganhe dinheiro rápido trabalhando de casa, sem experiência, cadastre-se grátis",
    "URGENTE: sua conta será bloqueada, confirme seus dados neste link",
    "Remédio com 80% de desconto, entrega discreta, compre agora",
    "Você foi selecionado para receber um iPhone grátis, clique e participe",
    "Aumente seus seguidores hoje mesmo, pacote promocional imperdível",
    "Last chance! Claim your free gift card now, click here",
    "Congratulations, you won the lottery, send your bank details to receive",
    "Make money fast from home, no experience needed, sign up free",
    "Cheap meds online, no prescription, limited time offer, buy now",
    "Your account has been suspended, verify your password immediately",
    "Dinheiro fácil! Invista R$ 100 e receba R$ 1.000 em 24 horas, garantido",
    "Cassino online: bônus de boas-vindas grátis, aposte agora e ganhe",
    "Atenção: fatura em atraso, pague agora neste link para evitar protesto",
    "Winner! You have been selected for an exclusive free vacation, call now",
    "Emagreça 10 kg em 7 dias com este método secreto, clique aqui",
    "Promoção relâmpago: 90% off em todos os produtos, acesse o link já",
    "Seu CPF foi sorteado, retire seu prêmio em dinheiro agora mesmo",
]

NAO_SPAM = [
    "Olá equipe, segue em anexo a ata da reunião de ontem para revisão",
    "Lembrete: reunião de planejamento amanhã às 10h na sala 3",
    "Bom dia, pode me enviar o relatório de vendas do mês passado?",
    "Obrigado pelo retorno, vou verificar os números e te respondo hoje",
    "Segue o contrato revisado conforme combinamos na ligação",
    "Podemos remarcar nossa call para quinta-feira à tarde?",
    "Oi Ana, enviei os arquivos do projeto na pasta compartilhada",
    "Confirmando o recebimento do pedido, a entrega será feita na sexta",
    "Hi team, please find the meeting notes attached",
    "Thanks for your email, I will review the proposal and get back to you",
    "Can we schedule a call for next week to discuss the project timeline?",
    "Reminder: the quarterly review is on Friday at 2 pm",
    "Segue o orçamento solicitado, qualquer dúvida estou à disposição",
    "Parabéns pelo excelente trabalho na apresentação de ontem",
    "Preciso da sua aprovação para o planejamento de campanhas do próximo trimestre",
    "O fornecedor confirmou o prazo de entrega para a próxima semana",
    "Anexei a planilha com as métricas de desempenho da campanha",
    "Vamos almoçar juntos amanhã para alinhar as próximas entregas?",
    "Please review the attached invoice and confirm the payment date",
    "Bom trabalho, equipe! A meta do mês foi atingida graças ao esforço de todos",
]


def dados_padrao() -> pd.DataFrame:
    """Monta um DataFrame com os exemplos embutidos no código."""
    textos = SPAM + NAO_SPAM
    rotulos = [1] * len(SPAM) + [0] * len(NAO_SPAM)
    return pd.DataFrame({"texto": textos, "rotulo": rotulos})


# ---------------------------------------------------------------------------
# 3) TREINO DO MODELO COM TENSORFLOW
# @st.cache_resource: o modelo é treinado uma vez e reaproveitado entre
# interações, em vez de retreinar a cada clique.
# O parâmetro é uma tupla (hashable) para o cache funcionar corretamente.
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="Treinando o modelo...")
def treinar_modelo(textos: tuple, rotulos: tuple):
    tf.keras.utils.set_random_seed(42)  # resultados reproduzíveis

    # Os textos viram um tensor do tipo string (tf.string). Um np.array de
    # texto tem dtype '<U...' (tamanho fixo), que o Keras 3 não aceita.
    x = tf.constant([str(t) for t in textos], dtype=tf.string)
    y = np.array(rotulos, dtype="float32")

    # Camada que converte texto em números (índices de palavras).
    vetorizador = tf.keras.layers.TextVectorization(
        max_tokens=5000, output_sequence_length=50, standardize="lower_and_strip_punctuation"
    )
    vetorizador.adapt(x)  # aprende o vocabulário a partir dos textos

    # Arquitetura: texto -> números -> embedding -> média -> decisão (0 a 1).
    modelo = tf.keras.Sequential(
        [
            tf.keras.Input(shape=(1,), dtype=tf.string),
            vetorizador,
            tf.keras.layers.Embedding(input_dim=5000, output_dim=16),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dropout(0.3),  # reduz overfitting
            tf.keras.layers.Dense(1, activation="sigmoid"),  # probabilidade de spam
        ]
    )
    modelo.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    modelo.fit(x, y, epochs=40, batch_size=8, verbose=0)
    return modelo


def prever(modelo, mensagem: str) -> float:
    """Retorna a probabilidade (0 a 1) de a mensagem ser spam."""
    entrada = tf.constant([mensagem], dtype=tf.string)  # mesmo tipo usado no treino
    return float(modelo.predict(entrada, verbose=0)[0][0])


# ---------------------------------------------------------------------------
# 4) BARRA LATERAL: dataset opcional enviado pelo usuário
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configurações")
    arquivo = st.file_uploader(
        "Treinar com seu próprio CSV (opcional)",
        type="csv",
        help="O arquivo precisa ter as colunas 'texto' e 'rotulo' (1 = spam, 0 = não spam).",
    )
    limiar = st.slider("Sensibilidade (limiar de spam)", 0.30, 0.90, 0.50, 0.05)
    st.caption("Quanto menor o limiar, mais mensagens serão marcadas como spam.")

# Escolhe a fonte dos dados: CSV enviado ou exemplos embutidos.
df = dados_padrao()
if arquivo is not None:
    try:
        df_csv = pd.read_csv(arquivo)
        if not {"texto", "rotulo"}.issubset(df_csv.columns):
            st.sidebar.error("O CSV precisa das colunas 'texto' e 'rotulo'.")
        else:
            df = df_csv.dropna(subset=["texto", "rotulo"])
            st.sidebar.success(f"{len(df)} mensagens carregadas.")
    except Exception as erro:
        st.sidebar.error(f"Não foi possível ler o CSV: {erro}")

modelo = treinar_modelo(tuple(df["texto"].astype(str)), tuple(df["rotulo"].astype(int)))

# ---------------------------------------------------------------------------
# 5) INTERFACE PRINCIPAL
# ---------------------------------------------------------------------------
st.title("📧 Detector de Spam")
st.write("Cole o conteúdo do e-mail abaixo para verificar se ele é spam.")

mensagem = st.text_area("Mensagem do e-mail", height=200, placeholder="Cole o texto aqui...")

if st.button("Analisar mensagem", type="primary"):
    if not mensagem.strip():
        st.warning("Digite ou cole uma mensagem antes de analisar.")
    else:
        prob = prever(modelo, mensagem)
        if prob >= limiar:
            st.error(f"🚨 **Possível SPAM** — probabilidade de {prob:.0%}")
        else:
            st.success(f"✅ **Não parece spam** — probabilidade de spam: {prob:.0%}")
        st.progress(prob)
        st.caption("O resultado é uma estimativa e deve apoiar, não substituir, a análise humana.")

st.divider()
st.caption(f"Modelo treinado com {len(df)} mensagens.")
