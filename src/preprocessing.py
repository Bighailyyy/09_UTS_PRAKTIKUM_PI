"""Text preprocessing: case folding, cleaning, tokenization, stopword removal,
dan (opsional) stemming Bahasa Indonesia berbasis aturan sederhana.

Hanya memakai pustaka standar Python.
"""
import re
import unicodedata
from typing import List

from .stopwords import STOPWORDS

_URL_RE = re.compile(r"(https?://\S+|www\.\S+)")
_HTML_RE = re.compile(r"<[^>]+>")
_TOKEN_RE = re.compile(r"[a-z0-9]+")


# --------------------------------------------------------------------------- #
# Stemmer sederhana (opsional). Sengaja konservatif: panjang stem minimal 5
# huruf untuk menghindari over-stemming. Bukan pengganti Sastrawi.
# --------------------------------------------------------------------------- #
_PARTICLES = ("lah", "kah", "pun")
_POSSESSIVE = ("nya",)
_DERIV_SUFFIX = ("an",)
_PREFIXES = ("meng", "meny", "mem", "men", "me", "peng", "peny", "pem", "pen",
             "ber", "per", "ter", "di", "ke", "se", "pe")
_MIN_STEM = 5


def stem_word(word: str) -> str:
    """Stemming Indonesia berbasis aturan (particle -> possessive -> suffix -> prefix)."""
    if len(word) <= _MIN_STEM or not word.isalpha():
        return word
    w = word
    for group in (_PARTICLES, _POSSESSIVE, _DERIV_SUFFIX):
        for suf in group:
            if w.endswith(suf) and len(w) - len(suf) >= _MIN_STEM:
                w = w[: -len(suf)]
                break
    for pre in _PREFIXES:
        if w.startswith(pre) and len(w) - len(pre) >= _MIN_STEM:
            w = w[len(pre):]
            break
    return w


# --------------------------------------------------------------------------- #
# Pipeline utama
# --------------------------------------------------------------------------- #
def case_fold(text: str) -> str:
    """Case folding + normalisasi unicode (hilangkan aksen)."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text.casefold()


def tokenize(text: str) -> List[str]:
    """Tokenisasi: buang URL/HTML, ambil deret alfanumerik."""
    text = _URL_RE.sub(" ", text)
    text = _HTML_RE.sub(" ", text)
    return _TOKEN_RE.findall(text)


def preprocess(text, use_stemming: bool = False, min_len: int = 2) -> List[str]:
    """Case folding -> tokenization -> stopword removal -> (stemming).

    Token angka murni dan token yang lebih pendek dari `min_len` dibuang.
    """
    if not isinstance(text, str) or not text:
        return []
    tokens = tokenize(case_fold(text))
    out = []
    for tok in tokens:
        if len(tok) < min_len or tok.isdigit() or tok in STOPWORDS:
            continue
        if use_stemming:
            tok = stem_word(tok)
            if tok in STOPWORDS:
                continue
        out.append(tok)
    return out


def preprocess_to_string(text, use_stemming: bool = False, min_len: int = 2) -> str:
    """Versi string (token digabung spasi) untuk disimpan di index Whoosh."""
    return " ".join(preprocess(text, use_stemming, min_len))
