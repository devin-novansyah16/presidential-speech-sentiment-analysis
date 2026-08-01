# 🎙️ Analisis Sentimen Pidato Presiden

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![NLP](https://img.shields.io/badge/NLP-Bahasa%20Indonesia-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

Proyek NLP end-to-end untuk menganalisis **sentimen dan topik** dari pidato
resmi kenegaraan, mulai dari pengumpulan data mentah sampai dashboard
interaktif siap pakai.

**Studi kasus:** Pidato Presiden Prabowo Subianto (sumber: setneg.go.id)

> **Catatan framing:** proyek ini murni analisis teknis linguistik/NLP —
> bagaimana tone dan topik berubah antar konteks pidato (kenegaraan, ekonomi,
> kabinet, dll). Ini **bukan** proyek penilaian atau opini politik.

---

## 📌 Daftar Isi

- [Fitur](#-fitur)
- [Alur Pipeline](#-alur-pipeline)
- [Struktur Proyek](#-struktur-proyek)
- [Instalasi & Cara Menjalankan](#-instalasi--cara-menjalankan)
- [Metodologi](#-metodologi)
- [Contoh Output](#-contoh-output)
- [Pengembangan Lanjutan](#-pengembangan-lanjutan)
- [Tech Stack](#-tech-stack)

## ✨ Fitur

- 🕸️ **Web scraping** transkrip pidato resmi dari setneg.go.id
- 🧹 **Preprocessing NLP Bahasa Indonesia** (cleaning, stopword removal, stemming dengan Sastrawi)
- 📊 **Sentiment analysis** berbasis lexicon (InSet Lexicon — 10.000+ kata berbobot)
- 🧩 **Topic modeling** otomatis dengan LDA (Latent Dirichlet Allocation)
- ☁️ **Word cloud** interaktif per label sentimen
- 📈 **Dashboard Streamlit** — distribusi sentimen, skor per pidato, dan eksplorasi topik, semuanya interaktif tanpa perlu coding ulang

## 🔄 Alur Pipeline

```
scraping (setneg.go.id)
        ↓
data mentah (raw_pidato.csv)
        ↓
preprocessing (cleaning → stopword removal → stemming)
        ↓
sentiment scoring (lexicon InSet, per-kalimat)
        ↓
topic modeling (LDA)
        ↓
dashboard interaktif (Streamlit)
```

## 📂 Struktur Proyek

```
pidato-sentiment/
├── data/
│   ├── positive.tsv          # InSet Lexicon - kata positif + bobot
│   ├── negative.tsv          # InSet Lexicon - kata negatif + bobot
│   ├── raw_pidato.csv        # data mentah hasil scraping (title, url, content)
│   └── pidato_analyzed.csv   # output akhir setelah pipeline dijalankan (auto-generated)
├── src/
│   ├── scraper.py            # ambil transkrip dari setneg.go.id
│   ├── preprocessing.py      # cleaning, stopword removal, stemming (Sastrawi)
│   ├── sentiment.py          # scoring sentimen berbasis lexicon InSet
│   └── analysis.py           # topic modeling (LDA) + agregasi tren
├── run_pipeline.py           # orkestrasi end-to-end
├── app.py                    # dashboard Streamlit
├── requirements.txt
└── TUTORIAL.md                # panduan detail langkah-demi-langkah
```

## 🚀 Instalasi & Cara Menjalankan

```bash
# 1. Clone repo ini
git clone https://github.com/<devin-novansyah16>/pidato-sentiment.git
cd pidato-sentiment

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Opsional) scraping data pidato terbaru
python src/scraper.py

# 4. Jalankan pipeline preprocessing + sentiment analysis
python run_pipeline.py

# 5. Buka dashboard
streamlit run app.py
```

Panduan lebih detail (termasuk troubleshooting) ada di [`TUTORIAL.md`](TUTORIAL.md).

## 🧠 Metodologi

| Tahap | Teknik |
|---|---|
| Preprocessing | Lowercasing, penghapusan URL/angka/simbol, stopword removal, stemming (Sastrawi) |
| Sentiment scoring | Lexicon-based — **InSet Lexicon** (Koto & Rahmaningtyas, 2017): 3.609 kata positif & 6.609 kata negatif dengan bobot -5 s.d. +5 |
| Granularitas | Per-kalimat (bukan per-pidato) agar analisis lebih detail dan timeline lebih bermakna |
| Topic modeling | Latent Dirichlet Allocation (scikit-learn), tanpa label manual |

## 📸 Contoh Output

> `![Dashboard](assets/dashboard-1)`
> `![Dashboard](assets/dashboard-screenshot.png)`
> `![Dashboard](assets/dashboard-screenshot.png)`
> `![Dashboard](assets/dashboard-screenshot.png)`

## 🔮 Pengembangan Lanjutan

- Bandingkan pendekatan lexicon dengan model **IndoBERT** fine-tuned untuk sentiment classification
- Tambahkan **Named Entity Recognition** untuk menandai isu/tokoh yang sering disebut per topik
- Bandingkan sentimen antar **konteks pidato** (ekonomi vs pertahanan vs sosial) sebagai fitur eksplorasi data

## 🛠️ Tech Stack

`Python` · `BeautifulSoup` · `Sastrawi` · `scikit-learn` · `pandas` · `Streamlit` · `WordCloud`

---

