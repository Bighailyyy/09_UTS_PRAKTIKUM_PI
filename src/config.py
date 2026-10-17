"""Konfigurasi global sistem IR."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "datasets"
INDEX_DIR = BASE_DIR / "index_dir"
META_FILE = INDEX_DIR / "meta.json"

# Lima dataset wajib (label tampilan). Nama file CSV dengan '_' maupun '-'
# dikenali, mis. etd-usk -> etd_usk.csv (lihat indexer.find_dataset_files).
DATASETS = ["etd-usk", "etd-ugm", "kompas", "tempo", "mojok"]

TITLE_COLUMN = "judul"
CONTENT_COLUMN = "konten"

# Parameter pencarian
TOP_K = 5               # jumlah dokumen yang ditampilkan ke pengguna
CANDIDATE_POOL = 200    # kandidat dari Whoosh yang di-rerank dengan cosine
TITLE_BOOST = 2.0       # bobot field judul pada tahap kandidat Whoosh
SNIPPET_CHARS = 220

# Parameter preprocessing (disimpan di meta index agar query konsisten)
USE_STEMMING = False
MIN_TOKEN_LEN = 2
