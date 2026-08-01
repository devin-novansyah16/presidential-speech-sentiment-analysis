"""
analysis.py
Analisis lanjutan: topic modeling (LDA) & agregasi tren sentimen.
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


def topic_modeling(texts: list[str], n_topics: int = 5, n_words: int = 8):
    """
    LDA sederhana untuk menemukan topik-topik utama yang dibahas di kumpulan pidato.
    Cocok dipakai setelah preprocessing (idealnya pada clean_text_nostop, TANPA stemming
    berlebihan supaya kata tetap mudah dibaca di output topik).
    """
    vectorizer = CountVectorizer(max_df=0.9, min_df=2, max_features=2000)
    dtm = vectorizer.fit_transform(texts)

    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)

    feature_names = vectorizer.get_feature_names_out()
    topics = {}
    for idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[-n_words:][::-1]]
        topics[f"Topik {idx + 1}"] = top_words
    return topics


def sentiment_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Ringkasan jumlah & proporsi label sentimen."""
    summary = df["sentiment_label"].value_counts().reset_index()
    summary.columns = ["label", "jumlah"]
    summary["persentase"] = (summary["jumlah"] / summary["jumlah"].sum() * 100).round(1)
    return summary


def sentiment_by_document(df: pd.DataFrame, title_col: str = "title") -> pd.DataFrame:
    """Skor sentimen rata-rata per pidato/dokumen -> untuk timeline atau perbandingan."""
    return (
        df.groupby(title_col)["sentiment_score"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "skor_rata_rata", "count": "jumlah_kalimat"})
        .sort_values("skor_rata_rata", ascending=False)
    )
