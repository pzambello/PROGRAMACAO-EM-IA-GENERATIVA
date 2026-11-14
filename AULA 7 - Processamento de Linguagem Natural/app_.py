import streamlit as st
from translate import Translator
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize

# Baixa os recursos do NLTK de forma segura
@st.cache_resource
def carregar_nltk():
    try:
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt_tab', quiet=True)
    except Exception:
        pass

carregar_nltk()

st.title('Análise de Sentimento')

texto = st.text_input('Digite um texto:')

if texto:
    # Passo 0: Traduzir para o inglês usando a biblioteca 'translate'
    try:
        tradutor = Translator(to_lang="en", from_lang="pt")
        texto_traduzido = tradutor.translate(texto)
    except Exception as e:
        texto_traduzido = texto
        st.error(f'Erro na tradução: {e}')

    # Passo 1: Tokenizar
    try:
        tokens = word_tokenize(texto, language='portuguese')
    except LookupError:
        tokens = texto.split()

    # Passo 2: Remover stop words
    try:
        stop_pt = set(stopwords.words('portuguese'))
    except LookupError:
        stop_pt = set()

    texto_limpo = [p for p in tokens if p.lower() not in stop_pt]

    st.write("**Original:**", texto)
    st.write("**Traduzido (para o VADER):**", texto_traduzido)
    st.write("**Tokens:**", tokens)
    st.write("**Limpo:**", texto_limpo)

    # Análise de sentimento utilizando o texto TRADUZIDO
    sia = SentimentIntensityAnalyzer()
    sentimento = sia.polarity_scores(texto_traduzido)

    st.write("**Scores detalhados:**", sentimento)

    score_ = sentimento['compound']

    if st.button('Analisar Sentimento'):
        if score_ >= 0.05:
            st.success('Positivo')
        elif score_ <= -0.05:
            st.error('Negativo')
        else:
            st.warning('Neutro')