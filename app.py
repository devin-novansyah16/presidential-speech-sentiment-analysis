"""
app.py
Dashboard Streamlit untuk analisis sentimen pidato.
Jalankan dengan: streamlit run app.py
"""

import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from src.analysis import sentiment_summary, sentiment_by_document, topic_modeling

st.set_page_config(page_title="Analisis Sentimen Pidato", layout="wide")
st.title("📊 Dashboard Analisis Sentimen Pidato")

DATA_PATH = "data/pidato_analyzed.csv"


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(
        f"File `{DATA_PATH}` belum ada. Jalankan `run_pipeline.py` terlebih dahulu "
        "untuk scraping -> preprocessing -> sentiment analysis."
    )
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Total pidato", df["title"].nunique())
col2.metric("Total kalimat dianalisis", len(df))
col3.metric(
    "Sentimen dominan",
    df["sentiment_label"].value_counts().idxmax().capitalize(),
)

st.subheader("Distribusi Sentimen")
summary = sentiment_summary(df)
st.bar_chart(summary.set_index("label")["jumlah"])
st.dataframe(summary, hide_index=True, use_container_width=True)

st.subheader("Skor Sentimen per Pidato")
per_doc = sentiment_by_document(df)
st.bar_chart(per_doc.set_index("title")["skor_rata_rata"])
st.dataframe(per_doc, hide_index=True, use_container_width=True)

st.subheader("Word Cloud")
sentiment_choice = st.selectbox("Pilih label sentimen", ["positif", "negatif", "netral"])
text_subset = " ".join(df[df["sentiment_label"] == sentiment_choice]["clean_text_nostop"].astype(str))
if text_subset.strip():
    wc = WordCloud(width=900, height=400, background_color="white").generate(text_subset)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
else:
    st.info("Tidak ada teks untuk label ini.")

st.subheader("Topik Utama (LDA)")
n_topics = st.slider("Jumlah topik", 2, 10, 5)
if st.button("Jalankan topic modeling"):
    texts = df["clean_text_nostop"].dropna().astype(str).tolist()
    topics = topic_modeling(texts, n_topics=n_topics)
    for topic_name, words in topics.items():
        st.write(f"**{topic_name}**: {', '.join(words)}")

st.subheader("Data Mentah")
st.dataframe(df[["title", "clean_text_nostop", "sentiment_score", "sentiment_label"]], use_container_width=True)
