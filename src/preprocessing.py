"""
preprocessing.py
Membersihkan & menormalisasi teks pidato Bahasa Indonesia sebelum dianalisis.
"""

import re
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

_stemmer = StemmerFactory().create_stemmer()
_stopword_remover = StopWordRemoverFactory().create_stop_word_remover()


def clean_text(text: str) -> str:
    """Lowercase, buang karakter non-huruf, rapikan spasi."""
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)   # buang URL
    text = re.sub(r"[^a-zA-Z\s]", " ", text)         # buang angka & simbol
    text = re.sub(r"\s+", " ", text).strip()
    return text


def remove_stopwords(text: str) -> str:
    return _stopword_remover.remove(text)


def stem_text(text: str) -> str:
    return _stemmer.stem(text)


def preprocess_pipeline(text: str, do_stem: bool = True) -> str:
    """
    Pipeline lengkap: clean -> stopword removal -> (opsional) stemming.
    Stemming lumayan berat secara komputasi untuk teks panjang (pidato bisa
    ribuan kata), jadi bisa dimatikan (do_stem=False) kalau ingin lebih cepat
    saat eksperimen awal.
    """
    text = clean_text(text)
    text = remove_stopwords(text)
    if do_stem:
        text = stem_text(text)
    return text


def split_sentences(text: str) -> list[str]:
    """Pecah pidato jadi kalimat, berguna untuk analisis sentimen per-kalimat
    (bukan cuma per-pidato) supaya timeline/detailnya lebih granular."""
    # split sederhana berdasarkan tanda baca akhir kalimat
    raw = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in raw if len(s.strip()) > 0]


def preprocess_dataframe(df: pd.DataFrame, text_col: str = "content", do_stem: bool = True) -> pd.DataFrame:
    """Terapkan preprocessing ke seluruh dataframe pidato."""
    df = df.copy()
    df["clean_text"] = df[text_col].astype(str).apply(clean_text)
    df["clean_text_nostop"] = df["clean_text"].apply(remove_stopwords)
    if do_stem:
        df["clean_text_stemmed"] = df["clean_text_nostop"].apply(stem_text)
    return df


if __name__ == "__main__":
    sample = "Saudara-saudara sekalian, kita harus swasembada pangan! Ini prioritas dasar bangsa kita."
    print("Original :", sample)
    print("Cleaned  :", clean_text(sample))
    print("No stop  :", remove_stopwords(clean_text(sample)))
    print("Stemmed  :", preprocess_pipeline(sample))
