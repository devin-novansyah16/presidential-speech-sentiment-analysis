"""
run_pipeline.py
Orkestrasi end-to-end: load data mentah -> preprocessing -> split kalimat
-> sentiment analysis -> simpan hasil ke data/pidato_analyzed.csv

Jalankan setelah data/raw_pidato.csv tersedia (hasil src/scraper.py, atau
kamu susun manual dari transkrip yang dikumpulkan sendiri).

Format data/raw_pidato.csv yang diharapkan (kolom):
    title, url, content
"""

import pandas as pd
from src.preprocessing import clean_text, remove_stopwords, split_sentences
from src.sentiment import analyze_dataframe

RAW_PATH = "data/raw_pidato.csv"
OUTPUT_PATH = "data/pidato_analyzed.csv"


def build_sentence_level_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Pecah tiap pidato jadi kalimat-kalimat, supaya skor sentimen lebih
    granular (bukan cuma 1 skor untuk 1 pidato yang panjangnya bisa ribuan kata).
    """
    rows = []
    for _, r in raw_df.iterrows():
        sentences = split_sentences(str(r["content"]))
        for s in sentences:
            rows.append({"title": r["title"], "url": r["url"], "content": s})
    return pd.DataFrame(rows)


def main():
    print(f"[1/4] Membaca {RAW_PATH} ...")
    raw_df = pd.read_csv(RAW_PATH)
    print(f"      {len(raw_df)} pidato ditemukan.")

    print("[2/4] Memecah jadi kalimat & membersihkan teks ...")
    sent_df = build_sentence_level_df(raw_df)
    sent_df["clean_text"] = sent_df["content"].astype(str).apply(clean_text)
    sent_df["clean_text_nostop"] = sent_df["clean_text"].apply(remove_stopwords)
    print(f"      {len(sent_df)} kalimat siap dianalisis.")

    print("[3/4] Menjalankan analisis sentimen (lexicon InSet) ...")
    result_df = analyze_dataframe(sent_df, text_col="clean_text_nostop")

    print(f"[4/4] Menyimpan hasil ke {OUTPUT_PATH} ...")
    result_df.to_csv(OUTPUT_PATH, index=False)
    print("Selesai. Jalankan `streamlit run app.py` untuk melihat dashboard.")


if __name__ == "__main__":
    main()
