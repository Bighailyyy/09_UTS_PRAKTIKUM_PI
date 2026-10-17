# Multi-Dataset Information Retrieval System (CLI)

Proyek UTS Praktikum Penelusuran Informasi - Departemen Informatika FMIPA, Universitas Syiah Kuala.

Sistem Information Retrieval berbasis *Command-Line Interface* yang mencari dan meranking dokumen dari
**5 dataset** sekaligus (49.484 dokumen):

| Dataset   | Sumber                              | Dokumen |
|-----------|-------------------------------------|--------:|
| `etd-usk` | Tesis/disertasi Universitas Syiah Kuala | 10.000 |
| `etd-ugm` | Tesis/disertasi Universitas Gadjah Mada | 10.000 |
| `kompas`  | Berita harian nasional              | 10.000 |
| `tempo`   | Majalah berita dan opini            | 10.000 |
| `mojok`   | Artikel populer dan satir           |  9.484 |

## Anggota Tim

Kelompok 09

| Nama | NPM | Bagian |
|------|-----|--------|
| Putroe Fatimah Azzahra | [2408107010002] | Preprocessing: `stopwords.py`, `preprocessing.py` |
| Fayla Syifa Rustam  | [2408107010029] | Indexing Whoosh: `config.py`, `indexer.py` |
| Annisa Rahma Fathia | [2408107010027] | Pencarian & ranking cosine, CLI: `searcher.py`, `main.py`, README |

## Fitur

- **Preprocessing**: case folding, tokenisasi, stopword removal (daftar Bahasa Indonesia + Inggris),
  dan stemming sederhana berbasis aturan (opsional).
- **Representasi dokumen**: Bag of Words dengan `CountVectorizer` (scikit-learn).
- **Indexing**: Whoosh (inverted index dengan field `title` dan `content`).
- **Pencarian & ranking**: kandidat diambil dari Whoosh (BM25F), lalu **diranking ulang dengan cosine similarity**
  antara vektor BoW query dan vektor BoW dokumen. Ditampilkan **5 dokumen teratas**.
- Filter pencarian per dataset (opsional).

## Struktur Folder

```
ir_system/
|- main.py              # CLI interaktif (entry point)
|- requirements.txt
|- README.md
|- src/
|  |- config.py         # parameter global (path, top-k, pool kandidat, dsb.)
|  |- stopwords.py      # daftar stopword
|  |- preprocessing.py  # case folding, tokenisasi, stopword removal, stemming
|  |- indexer.py        # membaca dataset & membangun index Whoosh
|  |- searcher.py       # pencarian Whoosh + BoW + cosine similarity
|- datasets/            # letakkan dataset di sini
|- index_dir/           # dibuat otomatis (index Whoosh + meta.json)
```

## Instalasi

Membutuhkan Python 3.9+ (diuji pada Python 3.12).

```bash
pip install -r requirements.txt
```

Hanya library standar Python + `scikit-learn`, `Whoosh`, dan `pandas` yang dipakai.

## Menyiapkan Dataset

Letakkan kelima dataset di folder `datasets/`. Format yang dikenali (CSV dengan kolom `judul` dan `konten`):

```
datasets/
|- etd_usk.csv      (atau etd-usk.csv, atau folder etd-usk/ berisi file .csv)
|- etd_ugm.csv
|- kompas.csv
|- tempo.csv
|- mojok.csv
```

Nama file dengan `_` maupun `-` dikenali. Folder `datasets/` di dalam zip pengumpulan sengaja dikosongkan
(ukuran dataset ±136 MB); salin file CSV dari `dataset.zip` ke dalamnya sebelum menjalankan sistem.

## Cara Menjalankan

```bash
python main.py
```

```
=== INFORMATION RETRIEVAL SYSTEM ===
[1] Load & Index Dataset
[2] Search Query
[3] Exit
====================================
```

1. **[1] Load & Index Dataset** - membangun index dari seluruh dataset (±2 menit untuk 49.484 dokumen pada 1 core CPU).
   Jika index sudah ada, pilih `L` untuk memuat ulang atau `r` untuk membangun ulang. Tersedia opsi membatasi jumlah
   dokumen per dataset (berguna untuk uji cepat) dan mengaktifkan stemming.
2. **[2] Search Query** - pilih filter dataset (Enter = semua), ketik query, dan sistem menampilkan 5 dokumen
   teratas beserta skor cosine, dataset asal, judul, dan cuplikan. Query kosong kembali ke menu.
3. **[3] Exit**.

### Contoh Output

Hasil nyata dari index penuh (49.484 dokumen), query `harga emas antam`:

```
  Top 5 hasil untuk: "harga emas antam"
  ----------------------------------------------------------------------------
  #1  cosine = 0.7701   [kompas]   (BM25F 79.18)
      Judul : Harga Emas Antam Hari Ini 19 Mei 2025 Kembali Melesat, Bagaimana dengan Harga Buyback?
      KOMPAS.com - Harga emas Antam hari ini Senin, 19 Mei 2025 yang dipantau
      dari laman Logam Mulia terpantau kembali melesat. ...
  ----------------------------------------------------------------------------
  #2  cosine = 0.7639   [tempo]   (BM25F 75.24)
      Judul : Daftar Harga Emas Antam dan UBS di Pegadaian 31 Maret 2025
      ...
  ----------------------------------------------------------------------------
```

Query `banjir bandang` menempatkan artikel Kompas "Banjir Bandang: Pengertian, Penyebab, dan Dampaknya"
di peringkat 1 (cosine 0,7722), disusul tesis UGM tentang kerentanan banjir bandang (cosine 0,6147).
Contoh query lain yang bisa dicoba: `sistem informasi akademik berbasis web`, `analisis sentimen twitter naive bayes`,
`rekomendasi lagu anime`.

## Pengujian Singkat

| Statistik | Nilai |
|-----------|-------|
| Dokumen terindeks | 49.484 |
| Term unik | 275.590 |
| Waktu build index | 131 detik |
| Ukuran index | 134 MB |
| Waktu pencarian | sekitar 0,15 - 0,32 detik/query |

Analisis lengkap (termasuk kasus gagal) ada di laporan PDF, Bab 4.

## Cara Kerja Singkat

**Indexing (menu 1)**

1. Baca CSV setiap dataset dengan pandas.
2. Preprocess judul dan isi: case folding -> tokenisasi (`[a-z0-9]+`, URL/HTML dibuang) -> buang stopword,
   angka murni, dan token < 2 karakter -> (stemming opsional).
3. Simpan ke Whoosh dengan skema: `doc_id`, `dataset`, `title` (terproses, searchable), `content` (judul+isi terproses,
   searchable dan *stored*), `title_raw` dan `snippet` (untuk tampilan).

**Pencarian (menu 2)**

1. Query dipreprocess dengan pipeline yang sama (pengaturan stemming dibaca dari `index_dir/meta.json`).
2. Whoosh mengambil hingga 200 kandidat dengan query OR atas seluruh term (field `title` diberi boost 2x), diurutkan BM25F.
3. Teks kandidat dan query diubah menjadi vektor BoW dengan `CountVectorizer`.
4. Skor akhir = `cosine_similarity(vektor_query, vektor_dokumen)`; urutkan menurun (tie-break dengan skor Whoosh),
   tampilkan Top 5.

Alasan desain dua tahap: Whoosh (inverted index) menyaring ±49 ribu dokumen menjadi kandidat secara efisien, sedangkan
cosine similarity pada representasi BoW menjadi penentu ranking akhir sesuai ketentuan tugas.

## Parameter (`src/config.py`)

| Parameter         | Default | Keterangan                                   |
|-------------------|--------:|----------------------------------------------|
| `TOP_K`           | 5       | Jumlah hasil yang ditampilkan                |
| `CANDIDATE_POOL`  | 200     | Jumlah kandidat Whoosh yang di-rerank        |
| `TITLE_BOOST`     | 2.0     | Bobot field judul pada tahap kandidat        |
| `USE_STEMMING`    | False   | Nilai awal stemming (dapat dipilih di menu 1)|
| `MIN_TOKEN_LEN`   | 2       | Panjang token minimum                        |

## Keterbatasan

- Cosine similarity memakai *raw term count* (tanpa IDF) sesuai ketentuan `CountVectorizer`, sehingga kata umum
  yang sering muncul (mis. "kerja") dapat mendominasi skor. Lihat Bab 5 laporan.
- Stemmer bawaan hanya aturan sederhana (tidak sekuat Sastrawi) dan dinonaktifkan secara default.
- Query diperlakukan sebagai *bag of words*; tidak ada pencarian frasa.

## Troubleshooting

| Pesan / masalah | Solusi |
|-----------------|--------|
| `'python' is not recognized` | Coba `py main.py` (Windows) atau `python3 main.py` (Mac/Linux) |
| `'pip' is not recognized` | Gunakan `python -m pip install -r requirements.txt` |
| `Dataset tidak ditemukan` | Pastikan kelima file CSV ada di folder `datasets/` dengan nama yang benar |
| `Index belum ada` | Jalankan menu `[1] Load & Index Dataset` sebelum menu `[2]` |
| Indexing terasa lama | Normal (sekitar 2 menit); untuk uji cepat batasi 500 dokumen per dataset |

