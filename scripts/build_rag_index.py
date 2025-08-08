"""Utility to build or update a simple vector index for RAG."""

import argparse
import json
import os
from pathlib import Path
from typing import List

import numpy as np
import openai

try:
    import faiss  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit("faiss library is required: %s" % exc)


def load_texts(data_dir: Path) -> List[str]:
    texts: List[str] = []
    for path in data_dir.glob("*.txt"):
        texts.append(path.read_text(encoding="utf-8"))
    return texts


def build_index(texts: List[str], out_path: Path) -> None:
    embeddings = []
    for txt in texts:
        resp = openai.Embedding.create(model="text-embedding-3-small", input=txt)
        embeddings.append(resp["data"][0]["embedding"])
    matrix = np.array(embeddings).astype("float32")
    index = faiss.IndexFlatL2(matrix.shape[1])
    index.add(matrix)
    faiss.write_index(index, str(out_path))
    with open(str(out_path) + ".meta", "w", encoding="utf-8") as f:
        json.dump(texts, f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build RAG vector index")
    parser.add_argument("data_dir", type=Path, help="Directory with .txt documents")
    parser.add_argument("out", type=Path, help="Path to save FAISS index")
    args = parser.parse_args()

    texts = load_texts(args.data_dir)
    if not texts:
        raise SystemExit("No .txt files found in data directory")
    build_index(texts, args.out)
    print(f"Index with {len(texts)} documents written to {args.out}")


if __name__ == "__main__":  # pragma: no cover
    main()
