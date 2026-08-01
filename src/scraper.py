"""
scraper.py
Mengambil daftar & isi pidato Presiden dari situs Sekretariat Negara (setneg.go.id).

Catatan penting:
- Situs setneg.go.id memuat pidato di halaman listing (listberita/pidato_presiden)
  dan detail di halaman /baca/index/<slug>.
- Struktur HTML bisa berubah sewaktu-waktu -> cek selector dengan `view page source`
  kalau scraping gagal / hasil kosong, lalu sesuaikan SELECTOR_* di bawah.
- Simpan hasil scraping mentah ke data/raw_pidato.csv supaya proses berikutnya
  (preprocessing, sentiment) tidak perlu scraping ulang tiap kali.
- Jalankan file ini secara LOKAL (bukan dari server cloud sandbox tertentu),
  sama seperti catatan submission ETL kamu sebelumnya, kalau situs targetnya
  memblokir request dari cloud/IP tertentu.
"""

import time
import csv
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.setneg.go.id"
LIST_URL = f"{BASE_URL}/listcontent/listberita/pidato_presiden"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}


def get_speech_links(list_url: str = LIST_URL, max_pages: int = 5) -> list[dict]:
    """
    Ambil daftar link + judul pidato dari halaman listing.
    Sesuaikan parameter pagination (mis. ?page=) dan selector <a> sesuai
    struktur HTML aktual saat kamu menjalankan ini.
    """
    links = []
    for page in range(1, max_pages + 1):
        url = f"{list_url}?page={page}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"[WARN] gagal ambil halaman {page}: status {resp.status_code}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")

        # TODO: sesuaikan selector ini dengan struktur HTML aktual halaman listing
        items = soup.select("a[href*='/baca/index/']")
        if not items:
            print(f"[INFO] tidak ada item lagi di halaman {page}, berhenti.")
            break

        for a in items:
            title = a.get_text(strip=True)
            href = a.get("href")
            if not href:
                continue
            full_url = href if href.startswith("http") else BASE_URL + href
            links.append({"title": title, "url": full_url})

        time.sleep(1)  # sopan terhadap server, hindari rate-limit

    # buang duplikat berdasarkan url
    seen = set()
    unique_links = []
    for item in links:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique_links.append(item)
    return unique_links



# Penanda bahwa kita sudah masuk ke bagian footer/arsip (di luar isi pidato).
# Begitu satu paragraf mengandung salah satu frasa ini, proses berhenti dan
# paragraf tsb + sesudahnya tidak diikutkan.
_STOP_MARKERS = [
    "sumber:",
    "arsip pidato",
    "humas kemensetneg",
    "copyrights",
]

# Paragraf yang lebih pendek dari ini dianggap noise (mis. "bagikan berita ke :").
_MIN_LEN = 3

# Paragraf yang PERSIS mengandung frasa ini adalah noise (tombol share, dsb),
# bukan bagian isi pidato - dibuang tapi tidak menghentikan proses (beda dengan
# _STOP_MARKERS yang menghentikan seluruhnya).
_NOISE_MARKERS = [
    "bagikan berita ke",
    "di baca",
]


def get_speech_content(url: str) -> str:
    """
    Ambil isi teks pidato dari halaman detail.

    Situs setneg.go.id tidak punya nama class yang stabil untuk container
    artikel, jadi daripada menebak selector (yang gampang basi kalau situs
    berubah), pendekatan di sini lebih robust:
    1. Ambil SEMUA tag <p> di halaman (setelah menghapus <script>/<style>/<nav>/
       <header>/<footer>).
    2. Berhenti mengumpulkan begitu ketemu paragraf yang menandakan sudah masuk
       ke bagian footer / arsip pidato lain (lihat _STOP_MARKERS), karena bagian
       itu selalu muncul tepat setelah isi pidato selesai.
    """
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()

    paragraphs = soup.find_all("p")

    collected = []
    for p in paragraphs:
        text = p.get_text(strip=True)
        if not text or len(text) < _MIN_LEN:
            continue

        lowered = text.lower()
        if any(marker in lowered for marker in _STOP_MARKERS):
            break
        if any(marker in lowered for marker in _NOISE_MARKERS):
            continue

        collected.append(text)

    return "\n".join(collected)


def scrape_all(output_csv: str = "data/raw_pidato.csv", max_pages: int = 5):
    links = get_speech_links(max_pages=max_pages)
    print(f"[INFO] ditemukan {len(links)} pidato, mulai mengambil isi...")

    rows = []
    for i, item in enumerate(links, 1):
        try:
            content = get_speech_content(item["url"])
            if content:
                rows.append({"title": item["title"], "url": item["url"], "content": content})
                print(f"[{i}/{len(links)}] OK: {item['title'][:60]}")
            else:
                print(f"[{i}/{len(links)}] SKIP (konten kosong): {item['title'][:60]}")
        except Exception as e:
            print(f"[{i}/{len(links)}] ERROR: {e}")
        time.sleep(1)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "url", "content"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"[DONE] {len(rows)} pidato disimpan ke {output_csv}")


if __name__ == "__main__":
    scrape_all()
