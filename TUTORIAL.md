# Tutorial: Cara Menjalankan Semua Skrip

Panduan ini mengasumsikan kamu sudah extract folder `pidato-sentiment/` dan
berada di terminal/command prompt dengan Python 3.10+ terinstall.

## 0. Masuk ke folder proyek

```bash
cd pidato-sentiment
```

## 1. Install semua dependency

```bash
pip install -r requirements.txt
```

Ini akan menginstall: `requests`, `beautifulsoup4`, `pandas`, `Sastrawi`,
`scikit-learn`, `wordcloud`, `matplotlib`, `streamlit`.

Kalau muncul error izin (permission), coba tambahkan `--user`:
```bash
pip install -r requirements.txt --user
```

## 2. (Opsional) Coba dulu dengan data contoh

Folder `data/raw_pidato.csv` sudah berisi 2 baris data contoh, jadi kamu bisa
langsung lompat ke **Langkah 4** untuk memastikan semua skrip jalan normal
sebelum repot cari data asli.

## 3. Kumpulkan data pidato asli

Pilih salah satu:

**Opsi A — Scraping otomatis**
```bash
python src/scraper.py
```
- Ini akan mengambil daftar & isi pidato dari setneg.go.id, lalu menyimpannya
  ke `data/raw_pidato.csv` (menimpa data contoh).
- Kalau hasilnya 0 pidato / error, kemungkinan besar struktur HTML situs
  sudah berubah. Buka `src/scraper.py`, cari komentar `# TODO`, lalu:
  1. Buka halaman listing pidato di browser, klik kanan → "Inspect"
  2. Cari nama class/tag yang membungkus link atau isi artikel
  3. Ganti selector di kode (`soup.select(...)` / `soup.select_one(...)`)
     sesuai yang kamu temukan

**Opsi B — Input manual**
1. Kumpulkan transkrip pidato (dari setneg.go.id, YouTube BPMI Setpres, atau
   media lain)
2. Buka `data/raw_pidato.csv` dengan spreadsheet/text editor
3. Isi baris baru dengan format: `title,url,content` (judul, sumber, isi
   pidato dalam satu baris — kalau ada koma di dalam teks, bungkus dengan
   tanda kutip `"..."`)
4. Simpan minimal 15-20 pidato untuk hasil analisis yang lebih bermakna

## 4. Jalankan pipeline preprocessing + sentiment analysis

```bash
python run_pipeline.py
```

Yang terjadi di balik layar:
1. Baca `data/raw_pidato.csv`
2. Pecah tiap pidato jadi kalimat-kalimat
3. Bersihkan teks (lowercase, hapus simbol/angka, hapus stopword)
4. Hitung skor sentimen tiap kalimat pakai lexicon InSet
5. Simpan hasil ke `data/pidato_analyzed.csv`

Kalau berhasil, kamu akan lihat output seperti:
```
[1/4] Membaca data/raw_pidato.csv ...
[2/4] Memecah jadi kalimat & membersihkan teks ...
[3/4] Menjalankan analisis sentimen (lexicon InSet) ...
[4/4] Menyimpan hasil ke data/pidato_analyzed.csv ...
Selesai. Jalankan `streamlit run app.py` untuk melihat dashboard.
```

## 5. Buka dashboard interaktif

```bash
streamlit run app.py
```

- Terminal akan menampilkan URL lokal (biasanya `http://localhost:8501`)
- Browser akan otomatis terbuka; kalau tidak, salin-tempel URL tersebut manual
- Di dashboard kamu bisa lihat: distribusi sentimen, skor per pidato, word
  cloud per label sentimen, dan topic modeling (klik tombol "Jalankan topic
  modeling" untuk generate topik)

## 6. (Opsional) Coba modul satu-satu

Setiap file di `src/` juga bisa dijalankan langsung untuk melihat contoh
kecilnya:

```bash
python src/preprocessing.py   # contoh cleaning teks
python src/sentiment.py       # contoh scoring sentimen
```

## Troubleshooting Singkat

| Masalah | Solusi |
|---|---|
| `ModuleNotFoundError` | Pastikan sudah `pip install -r requirements.txt` dan berada di folder `pidato-sentiment/` |
| Scraper hasil 0 data | Selector HTML perlu disesuaikan (lihat Langkah 3, Opsi A) |
| `FileNotFoundError: data/pidato_analyzed.csv` saat buka dashboard | Jalankan `python run_pipeline.py` dulu sebelum `streamlit run app.py` |
| Streamlit tidak auto-buka browser | Salin URL dari terminal, buka manual di browser |
