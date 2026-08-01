"""
sentiment.py
Analisis sentimen berbasis lexicon (InSet Lexicon - Koto & Rahmaningtyas, 2017).
Setiap kata dicocokkan dengan bobot pada lexicon positif/negatif, lalu dijumlah
untuk mendapat skor sentimen per teks (kalimat / pidato).
"""

import pandas as pd

POSITIVE_PATH = "data/positive.tsv"
NEGATIVE_PATH = "data/negative.tsv"


def load_lexicon(pos_path: str = POSITIVE_PATH, neg_path: str = NEGATIVE_PATH) -> dict:
    pos_df = pd.read_csv(pos_path, sep="\t")
    neg_df = pd.read_csv(neg_path, sep="\t")

    lexicon = {}
    for _, row in pos_df.iterrows():
        lexicon[row["word"]] = row["weight"]
    for _, row in neg_df.iterrows():
        lexicon[row["word"]] = row["weight"]  # weight negatif sudah berupa angka negatif
    return lexicon


def score_text(text: str, lexicon: dict) -> float:
    """Jumlahkan bobot tiap kata yang ada di lexicon. Kata di luar lexicon diabaikan."""
    words = text.split()
    score = sum(lexicon.get(w, 0) for w in words)
    return score


def label_from_score(score: float) -> str:
    if score > 0:
        return "positif"
    elif score < 0:
        return "negatif"
    return "netral"


def analyze_dataframe(df: pd.DataFrame, text_col: str = "clean_text_nostop") -> pd.DataFrame:
    """Tambahkan kolom sentiment_score dan sentiment_label ke dataframe."""
    lexicon = load_lexicon()
    df = df.copy()
    df["sentiment_score"] = df[text_col].astype(str).apply(lambda t: score_text(t, lexicon))
    df["sentiment_label"] = df["sentiment_score"].apply(label_from_score)
    return df


if __name__ == "__main__":
    lex = load_lexicon()
    contoh = "kita harus bersatu dan bekerja keras untuk kemajuan bangsa"
    s = score_text(contoh, lex)
    print(f"Teks: {contoh}")
    print(f"Skor: {s} -> Label: {label_from_score(s)}")
