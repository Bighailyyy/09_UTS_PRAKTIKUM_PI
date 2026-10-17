"""Pencarian: kandidat dari Whoosh (BM25F) -> representasi BoW (CountVectorizer)
-> ranking akhir dengan cosine similarity."""
from dataclasses import dataclass
from typing import List, Optional

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from whoosh.query import Or, Term

from . import config
from .indexer import load_meta, open_index
from .preprocessing import preprocess


@dataclass
class SearchResult:
    rank: int
    doc_id: str
    dataset: str
    title: str
    snippet: str
    cosine: float
    whoosh_score: float


class Searcher:
    def __init__(self):
        self.ix = open_index()
        self.meta = load_meta()
        self.use_stemming = bool(self.meta.get("use_stemming", config.USE_STEMMING))

    def close(self):
        self.ix.close()

    # ------------------------------------------------------------------ #
    def _build_query(self, tokens: List[str]):
        clauses = []
        for t in dict.fromkeys(tokens):  # unik, urutan terjaga
            clauses.append(Term("content", t))
            clauses.append(Term("title", t, boost=config.TITLE_BOOST))
        return Or(clauses)

    def search(self, query: str, top_k: int = config.TOP_K,
               dataset: Optional[str] = None,
               pool: int = config.CANDIDATE_POOL) -> List[SearchResult]:
        tokens = preprocess(query, self.use_stemming, config.MIN_TOKEN_LEN)
        if not tokens:
            return []

        flt = Term("dataset", dataset) if dataset else None
        with self.ix.searcher() as s:
            hits = s.search(self._build_query(tokens), limit=pool, filter=flt)
            if len(hits) == 0:
                return []
            cands = [(h["doc_id"], h["dataset"], h["title_raw"], h["snippet"],
                      h["content"], float(h.score)) for h in hits]

        # --- Bag of Words + cosine similarity ---------------------------------
        vec = CountVectorizer(tokenizer=str.split, preprocessor=None,
                              lowercase=False, token_pattern=None)
        doc_matrix = vec.fit_transform([c[4] for c in cands])
        q_vec = vec.transform([" ".join(tokens)])
        sims = cosine_similarity(q_vec, doc_matrix).ravel()

        order = sorted(range(len(cands)), key=lambda i: (-sims[i], -cands[i][5]))
        results = []
        for rank, i in enumerate(order[:top_k], start=1):
            doc_id, ds, title, snip, _, wscore = cands[i]
            results.append(SearchResult(rank, doc_id, ds, title, snip,
                                        float(sims[i]), wscore))
        return results
