"""Pembentukan index Whoosh dari lima dataset (CSV: kolom `judul`, `konten`)."""
import json
import re
import shutil
import time
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
from whoosh import index
from whoosh.analysis import RegexTokenizer
from whoosh.fields import ID, STORED, TEXT, Schema

from . import config
from .preprocessing import preprocess_to_string

# Analyzer: teks sudah dipreprocess oleh pipeline kita, jadi Whoosh cukup
# memecah berdasarkan spasi (tanpa filter tambahan).
WS_ANALYZER = RegexTokenizer(r"\S+")


def build_schema() -> Schema:
    return Schema(
        doc_id=ID(stored=True, unique=True),
        dataset=ID(stored=True),
        title=TEXT(analyzer=WS_ANALYZER, phrase=False),        # judul terproses (searchable)
        content=TEXT(analyzer=WS_ANALYZER, phrase=False, stored=True),  # judul+isi terproses
        title_raw=STORED,                                      # judul asli (tampilan)
        snippet=STORED,                                        # cuplikan isi asli
    )


def _norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def find_dataset_files(dataset_dir: Path) -> Dict[str, Path]:
    """Petakan label dataset -> file CSV. Mendukung `etd_usk.csv`, `etd-usk.csv`,
    atau folder `etd-usk/` yang berisi satu/lebih file CSV."""
    found: Dict[str, Path] = {}
    for label in config.DATASETS:
        for p in sorted(dataset_dir.rglob("*.csv")):
            stem = p.stem if p.parent == dataset_dir else p.parent.name
            if _norm(stem) == _norm(label):
                found[label] = p
                break
    return found


def read_dataset(path: Path, limit: Optional[int] = None) -> pd.DataFrame:
    df = pd.read_csv(path, nrows=limit)
    df[config.TITLE_COLUMN] = df[config.TITLE_COLUMN].fillna("").astype(str)
    df[config.CONTENT_COLUMN] = df[config.CONTENT_COLUMN].fillna("").astype(str)
    return df


def index_exists() -> bool:
    return config.INDEX_DIR.exists() and index.exists_in(str(config.INDEX_DIR))


def load_meta() -> dict:
    if config.META_FILE.exists():
        return json.loads(config.META_FILE.read_text(encoding="utf-8"))
    return {}


def build_index(limit_per_dataset: Optional[int] = None,
                use_stemming: bool = config.USE_STEMMING,
                log=print) -> dict:
    """Bangun index dari seluruh dataset. Mengembalikan statistik."""
    files = find_dataset_files(config.DATASET_DIR)
    missing = [d for d in config.DATASETS if d not in files]
    if missing:
        raise FileNotFoundError(
            f"Dataset tidak ditemukan di {config.DATASET_DIR}: {', '.join(missing)}")

    if config.INDEX_DIR.exists():
        shutil.rmtree(config.INDEX_DIR)
    config.INDEX_DIR.mkdir(parents=True)
    ix = index.create_in(str(config.INDEX_DIR), build_schema())
    writer = ix.writer(limitmb=256, procs=1)

    stats = {"per_dataset": {}, "use_stemming": use_stemming}
    t0 = time.time()
    total = 0
    for label in config.DATASETS:
        t1 = time.time()
        df = read_dataset(files[label], limit_per_dataset)
        n = 0
        for row_id, (title, body) in enumerate(
                zip(df[config.TITLE_COLUMN], df[config.CONTENT_COLUMN])):
            title_p = preprocess_to_string(title, use_stemming, config.MIN_TOKEN_LEN)
            body_p = preprocess_to_string(body, use_stemming, config.MIN_TOKEN_LEN)
            if not title_p and not body_p:
                continue
            writer.add_document(
                doc_id=f"{label}-{row_id}",
                dataset=label,
                title=title_p,
                content=(title_p + " " + body_p).strip(),
                title_raw=title.strip(),
                snippet=" ".join(body.split())[: config.SNIPPET_CHARS],
            )
            n += 1
        stats["per_dataset"][label] = n
        total += n
        log(f"  [+] {label:<8} {n:>6} dokumen  ({time.time() - t1:5.1f} dtk)")

    log("  Menyimpan (commit) index ke disk ...")
    writer.commit()
    stats["total_docs"] = total
    stats["build_seconds"] = round(time.time() - t0, 1)
    config.META_FILE.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    return stats


def open_index():
    return index.open_dir(str(config.INDEX_DIR))
