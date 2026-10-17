#!/usr/bin/env python3
"""Multi-Dataset Information Retrieval System (CLI).

Jalankan:  python main.py
"""
import textwrap

from src import config
from src.indexer import build_index, index_exists, load_meta
from src.searcher import Searcher

MENU = """
=== INFORMATION RETRIEVAL SYSTEM ===
[1] Load & Index Dataset
[2] Search Query
[3] Exit
===================================="""


def print_stats(stats: dict):
    print("\n  Ringkasan index:")
    for name, n in stats.get("per_dataset", {}).items():
        print(f"    - {name:<8}: {n:>6} dokumen")
    print(f"    Total        : {stats.get('total_docs', 0)} dokumen")
    if "build_seconds" in stats:
        print(f"    Waktu build  : {stats['build_seconds']} detik")
    print(f"    Stemming     : {'ya' if stats.get('use_stemming') else 'tidak'}")


def action_index():
    if index_exists():
        ans = input("Index sudah ada. [L]oad index yang ada atau [R]ebuild? (L/r): ").strip().lower()
        if ans != "r":
            print_stats(load_meta())
            print("\n  Index siap digunakan.")
            return
    lim = input("Batasi jumlah dokumen per dataset? (Enter = semua): ").strip()
    limit = int(lim) if lim.isdigit() and int(lim) > 0 else None
    stem = input("Aktifkan stemming sederhana? (y/N): ").strip().lower() == "y"
    print("\n  Membangun index (preprocessing + Whoosh) ...")
    try:
        stats = build_index(limit_per_dataset=limit, use_stemming=stem)
    except FileNotFoundError as e:
        print(f"\n  [!] {e}")
        return
    print_stats(stats)
    print("\n  Index selesai dibuat.")


def show_results(results, query):
    print(f"\n  Top {len(results)} hasil untuk: \"{query}\"")
    print("  " + "-" * 76)
    for r in results:
        print(f"  #{r.rank}  cosine = {r.cosine:.4f}   [{r.dataset}]   (BM25F {r.whoosh_score:.2f})")
        print(f"      Judul : {textwrap.shorten(r.title, 90)}")
        for line in textwrap.wrap(r.snippet, 72)[:3]:
            print(f"      {line}")
        print("  " + "-" * 76)


def action_search(searcher):
    if searcher[0] is None:
        if not index_exists():
            print("\n  [!] Index belum ada. Jalankan menu [1] terlebih dahulu.")
            return
        searcher[0] = Searcher()
    s = searcher[0]
    print("\n  Dataset: " + ", ".join(config.DATASETS))
    ds = input("  Filter dataset (Enter = semua): ").strip().lower() or None
    if ds and ds not in config.DATASETS:
        print(f"  [!] Dataset '{ds}' tidak dikenal, mencari di semua dataset.")
        ds = None
    while True:
        q = input("\n  Query (kosong = kembali ke menu): ").strip()
        if not q:
            return
        results = s.search(q, dataset=ds)
        if not results:
            print("  Tidak ada dokumen yang cocok (atau query hanya berisi stopword).")
        else:
            show_results(results, q)


def main():
    searcher = [None]
    while True:
        print(MENU)
        choice = input("Pilih menu [1-3]: ").strip()
        if choice == "1":
            if searcher[0] is not None:
                searcher[0].close()
                searcher[0] = None
            action_index()
        elif choice == "2":
            action_search(searcher)
        elif choice == "3":
            print("Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSampai jumpa!")
