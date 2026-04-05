#!/usr/bin/env python3
"""Pre-compute BM25 and semantic embedding indexes for the memory store.

Run this after extracting new sessions to ensure search is fast.
Cached indexes are stored in memory/.cache/ and loaded automatically by search.py.
"""

import argparse
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "memory"))

from search import MemorySearcher, load_documents, CACHE_DIR, EMBEDDING_CACHE, INDEX_CACHE


def main():
    parser = argparse.ArgumentParser(description="Build search indexes for long-term memory")
    parser.add_argument("--skip-embeddings", action="store_true",
                        help="Only build BM25 index (skip slow embedding computation)")
    parser.add_argument("--force", action="store_true",
                        help="Rebuild even if cache exists")
    args = parser.parse_args()

    docs = load_documents()
    if not docs:
        print("No documents found in memory store. Run extract-sessions.py first.")
        sys.exit(1)

    print(f"Found {len(docs)} documents in memory store")

    if args.force:
        for cache_file in [INDEX_CACHE, EMBEDDING_CACHE]:
            if cache_file.exists():
                cache_file.unlink()
                print(f"  Removed stale cache: {cache_file.name}")

    searcher = MemorySearcher(docs)

    print("\nBuilding BM25 index...")
    t0 = time.time()
    searcher._ensure_bm25()
    searcher.save_index()
    bm25_time = time.time() - t0
    print(f"  BM25 index built in {bm25_time:.2f}s ({len(docs)} documents)")

    if not args.skip_embeddings:
        print("\nBuilding semantic embeddings...")
        t0 = time.time()
        searcher._ensure_embeddings()
        emb_time = time.time() - t0
        print(f"  Embeddings built in {emb_time:.2f}s ({len(docs)} documents)")
    else:
        print("\nSkipping embeddings (--skip-embeddings)")

    bm25_size = INDEX_CACHE.stat().st_size if INDEX_CACHE.exists() else 0
    emb_size = EMBEDDING_CACHE.stat().st_size if EMBEDDING_CACHE.exists() else 0
    print(f"\nCache sizes:")
    print(f"  BM25 index: {bm25_size / 1024:.1f} KB")
    print(f"  Embeddings: {emb_size / 1024:.1f} KB")
    print("\nIndex build complete.")


if __name__ == "__main__":
    main()
