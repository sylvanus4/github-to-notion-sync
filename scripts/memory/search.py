#!/usr/bin/env python3
"""Hybrid search over the project's long-term memory store.

Modes:
  bm25     — Fast keyword search (BM25Okapi)
  semantic — Embedding-based conceptual search
  hybrid   — Weighted RRF fusion of BM25 + semantic (default)
  temporal — Date-filtered session scan
  skills   — Search existing SKILL.md files for similarity (used by autoskill-judge)
"""

import argparse
import json
import os
import pickle
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MEMORY_DIR = PROJECT_ROOT / "memory"
SESSIONS_DIR = MEMORY_DIR / "sessions"
CACHE_DIR = MEMORY_DIR / ".cache"
EMBEDDING_CACHE = CACHE_DIR / "embeddings.pkl"
INDEX_CACHE = CACHE_DIR / "index.pkl"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
DEFAULT_MODEL = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from markdown."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    fm_text = match.group(1)
    body = text[match.end():]
    meta = {}
    current_key = None
    list_values = []

    for line in fm_text.splitlines():
        if line.startswith("  - "):
            list_values.append(line.strip("- ").strip())
        elif ":" in line:
            if current_key and list_values:
                meta[current_key] = list_values
                list_values = []
            key, _, val = line.partition(":")
            current_key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val and val != "[]":
                meta[current_key] = val
        else:
            if current_key and list_values:
                meta[current_key] = list_values
                list_values = []

    if current_key and list_values:
        meta[current_key] = list_values

    return meta, body


def load_documents() -> list[dict]:
    """Load all markdown documents from the memory store."""
    docs = []

    md_dirs = [SESSIONS_DIR, MEMORY_DIR]
    for search_dir in md_dirs:
        if not search_dir.exists():
            continue
        for md_file in sorted(search_dir.glob("*.md")):
            if md_file.name.startswith(".") or md_file.name == "index.md":
                continue
            text = md_file.read_text()
            meta, body = parse_frontmatter(text)
            docs.append({
                "path": str(md_file.relative_to(PROJECT_ROOT)),
                "filename": md_file.name,
                "title": meta.get("title", md_file.stem),
                "date": meta.get("date", ""),
                "type": meta.get("type", "document"),
                "session_id": meta.get("session_id", ""),
                "messages": int(meta.get("messages", 0)) if meta.get("messages") else 0,
                "body": body.strip(),
                "full_text": f"{meta.get('title', '')} {body.strip()}",
            })

    return docs


def tokenize(text: str) -> list[str]:
    """Simple whitespace + punctuation tokenizer for mixed English/Korean text."""
    text = text.lower()
    text = re.sub(r"[^\w\s가-힣]", " ", text)
    tokens = text.split()
    return [t for t in tokens if len(t) > 1]


class MemorySearcher:
    """Multi-mode search engine over the memory store."""

    def __init__(self, docs: Optional[list[dict]] = None):
        self.docs = docs or load_documents()
        self._bm25 = None
        self._corpus = None
        self._embeddings = None
        self._model = None
        self._load_cache()

    def _load_cache(self) -> None:
        if INDEX_CACHE.exists():
            try:
                cache = pickle.loads(INDEX_CACHE.read_bytes())
                cached_paths = set(cache.get("paths", []))
                current_paths = {d["path"] for d in self.docs}
                if cached_paths == current_paths:
                    self._bm25 = cache.get("bm25")
                    self._corpus = cache.get("corpus")
            except Exception:
                pass

        if EMBEDDING_CACHE.exists():
            try:
                emb_cache = pickle.loads(EMBEDDING_CACHE.read_bytes())
                cached_paths = set(emb_cache.get("paths", []))
                current_paths = {d["path"] for d in self.docs}
                if cached_paths == current_paths:
                    self._embeddings = emb_cache.get("embeddings")
            except Exception:
                pass

    def _ensure_bm25(self) -> None:
        if self._bm25 is not None:
            return
        from rank_bm25 import BM25Okapi
        self._corpus = [tokenize(d["full_text"]) for d in self.docs]
        if self._corpus:
            self._bm25 = BM25Okapi(self._corpus)

    def _ensure_embeddings(self) -> None:
        if self._embeddings is not None:
            return
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(DEFAULT_MODEL)
        texts = [d["full_text"] for d in self.docs]
        self._embeddings = self._model.encode(texts, show_progress_bar=True)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        EMBEDDING_CACHE.write_bytes(pickle.dumps({
            "paths": [d["path"] for d in self.docs],
            "embeddings": self._embeddings,
        }))

    def save_index(self) -> None:
        """Persist the BM25 index to disk."""
        self._ensure_bm25()
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        INDEX_CACHE.write_bytes(pickle.dumps({
            "paths": [d["path"] for d in self.docs],
            "bm25": self._bm25,
            "corpus": self._corpus,
        }))

    def search_bm25(self, query: str, top_n: int = 5) -> list[dict]:
        self._ensure_bm25()
        if not self._bm25:
            return []
        query_tokens = tokenize(query)
        scores = self._bm25.get_scores(query_tokens)
        ranked = np.argsort(scores)[::-1][:top_n]
        results = []
        for idx in ranked:
            if scores[idx] > 0:
                doc = self.docs[idx].copy()
                doc["_score"] = float(scores[idx])
                doc["_mode"] = "bm25"
                results.append(doc)
        return results

    def search_semantic(self, query: str, top_n: int = 5) -> list[dict]:
        self._ensure_embeddings()
        from sklearn.metrics.pairwise import cosine_similarity
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(DEFAULT_MODEL)
        query_emb = self._model.encode([query], show_progress_bar=False)
        sims = cosine_similarity(query_emb, self._embeddings)[0]
        ranked = np.argsort(sims)[::-1][:top_n]
        results = []
        for idx in ranked:
            if sims[idx] > 0.1:
                doc = self.docs[idx].copy()
                doc["_score"] = float(sims[idx])
                doc["_mode"] = "semantic"
                results.append(doc)
        return results

    def search_hybrid(self, query: str, top_n: int = 5, k: int = 60) -> list[dict]:
        """RRF fusion of BM25 + semantic results."""
        self._ensure_bm25()
        self._ensure_embeddings()

        from sklearn.metrics.pairwise import cosine_similarity

        query_tokens = tokenize(query)
        bm25_scores = self._bm25.get_scores(query_tokens)
        bm25_rank = np.argsort(bm25_scores)[::-1].tolist()

        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(DEFAULT_MODEL)
        query_emb = self._model.encode([query], show_progress_bar=False)
        sims = cosine_similarity(query_emb, self._embeddings)[0]
        sem_rank = np.argsort(sims)[::-1].tolist()

        rrf_scores = {}
        for rank_list in [bm25_rank, sem_rank]:
            for rank, idx in enumerate(rank_list):
                if idx not in rrf_scores:
                    rrf_scores[idx] = 0.0
                rrf_scores[idx] += 1.0 / (k + rank + 1)

        sorted_indices = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in sorted_indices[:top_n]:
            if bm25_scores[idx] > 0 or sims[idx] > 0.1:
                doc = self.docs[idx].copy()
                doc["_score"] = score
                doc["_bm25_score"] = float(bm25_scores[idx])
                doc["_semantic_score"] = float(sims[idx])
                doc["_mode"] = "hybrid"
                results.append(doc)
        return results

    def search_temporal(self, date_str: str = "", days: int = 1, top_n: int = 10) -> list[dict]:
        """Filter sessions by date range."""
        if date_str == "yesterday":
            target = datetime.now() - timedelta(days=1)
            date_str = target.strftime("%Y-%m-%d")
            days = 1
        elif date_str == "today":
            date_str = datetime.now().strftime("%Y-%m-%d")
            days = 1
        elif date_str == "last week":
            target = datetime.now() - timedelta(days=7)
            date_str = target.strftime("%Y-%m-%d")
            days = 7

        try:
            start_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            start_date = datetime.now() - timedelta(days=days)

        end_date = start_date + timedelta(days=days)

        results = []
        for doc in self.docs:
            if not doc.get("date"):
                continue
            try:
                doc_date = datetime.strptime(doc["date"], "%Y-%m-%d")
            except ValueError:
                continue
            if start_date <= doc_date < end_date:
                doc_copy = doc.copy()
                doc_copy["_score"] = 1.0
                doc_copy["_mode"] = "temporal"
                results.append(doc_copy)

        results.sort(key=lambda d: d.get("date", ""), reverse=True)
        return results[:top_n]

    def search_skills(self, query: str, top_n: int = 3) -> list[dict]:
        """Search existing SKILL.md files for similarity to a candidate.

        Used by autoskill-judge to find skills that might overlap with
        a newly extracted candidate.
        """
        skills_dir = PROJECT_ROOT / ".cursor" / "skills"
        if not skills_dir.exists():
            return []

        skill_docs = []
        for skill_dir in sorted(skills_dir.iterdir()):
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue
            text = skill_file.read_text()
            _, body = parse_frontmatter(text)
            first_line = body.strip().split("\n")[0].lstrip("# ").strip() if body.strip() else skill_dir.name
            desc_lines = [l for l in body.strip().split("\n")[1:6] if l.strip()]
            description = " ".join(desc_lines)
            skill_docs.append({
                "path": str(skill_file.relative_to(PROJECT_ROOT)),
                "name": skill_dir.name,
                "title": first_line,
                "description": description,
                "full_text": f"{first_line} {description}",
                "body": body.strip(),
            })

        if not skill_docs:
            return []

        from rank_bm25 import BM25Okapi

        corpus = [tokenize(d["full_text"]) for d in skill_docs]
        bm25 = BM25Okapi(corpus)
        query_tokens = tokenize(query)
        scores = bm25.get_scores(query_tokens)
        ranked = np.argsort(scores)[::-1][:top_n]

        results = []
        for idx in ranked:
            if scores[idx] > 0:
                doc = skill_docs[idx].copy()
                doc["_score"] = float(scores[idx])
                doc["_mode"] = "skill-search"
                results.append(doc)
        return results

    def search(self, query: str, mode: str = "hybrid", top_n: int = 5, **kwargs) -> list[dict]:
        """Unified search dispatcher."""
        if mode == "bm25":
            return self.search_bm25(query, top_n)
        elif mode == "semantic":
            return self.search_semantic(query, top_n)
        elif mode == "hybrid":
            return self.search_hybrid(query, top_n)
        elif mode == "temporal":
            return self.search_temporal(query, top_n=top_n, **kwargs)
        elif mode == "skills":
            return self.search_skills(query, top_n)
        else:
            raise ValueError(f"Unknown mode: {mode}. Use bm25, semantic, hybrid, temporal, or skills.")


def format_result(doc: dict, index: int, verbose: bool = False) -> str:
    """Format a single search result for display."""
    lines = [
        f"[{index}] {doc.get('title', 'Untitled')}",
        f"    Path: {doc['path']}",
        f"    Date: {doc.get('date', 'N/A')} | Type: {doc.get('type', 'N/A')} | Score: {doc['_score']:.4f}",
    ]
    if verbose:
        body_preview = doc.get("body", "")[:300].replace("\n", " ")
        lines.append(f"    Preview: {body_preview}...")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Search the project's long-term memory")
    parser.add_argument("query", nargs="?", default="", help="Search query")
    parser.add_argument("--mode", choices=["bm25", "semantic", "hybrid", "temporal", "skills"], default="hybrid")
    parser.add_argument("--top", type=int, default=5, help="Number of results")
    parser.add_argument("--date", type=str, default="", help="Date for temporal search (YYYY-MM-DD, yesterday, today, last week)")
    parser.add_argument("--days", type=int, default=1, help="Number of days for temporal range")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.mode == "temporal":
        query = args.date or args.query
    elif args.mode == "skills":
        if not args.query:
            print("Error: query is required for skill search", file=sys.stderr)
            sys.exit(1)
        query = args.query
    else:
        if not args.query:
            print("Error: query is required for non-temporal search", file=sys.stderr)
            sys.exit(1)
        query = args.query

    searcher = MemorySearcher()
    print(f"Loaded {len(searcher.docs)} documents from memory store", file=sys.stderr)

    if args.mode == "temporal":
        results = searcher.search_temporal(query, days=args.days, top_n=args.top)
    elif args.mode == "skills":
        results = searcher.search_skills(query, top_n=args.top)
    else:
        results = searcher.search(query, mode=args.mode, top_n=args.top)

    if args.json:
        output = []
        for r in results:
            output.append({
                "path": r["path"],
                "title": r.get("title", ""),
                "date": r.get("date", ""),
                "score": r["_score"],
                "mode": r["_mode"],
                "body_preview": r.get("body", "")[:500],
            })
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        if not results:
            print("No results found.")
        else:
            print(f"\n{'='*60}")
            print(f"  {len(results)} results for: \"{query}\" (mode={args.mode})")
            print(f"{'='*60}\n")
            for i, doc in enumerate(results, 1):
                print(format_result(doc, i, verbose=args.verbose))
                print()


if __name__ == "__main__":
    main()
