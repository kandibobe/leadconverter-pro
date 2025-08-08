from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import numpy as np
import openai

try:  # optional dependency
    import faiss  # type: ignore
except Exception:  # pragma: no cover
    faiss = None

INDEX_PATH = os.environ.get("RAG_INDEX_PATH", "rag_index.faiss")
META_PATH = os.environ.get("RAG_META_PATH", "rag_index.meta")

_rag_index = None
_rag_texts: List[str] = []


def load_rag_index() -> None:
    """Load FAISS index from disk if available."""
    global _rag_index, _rag_texts
    if faiss is None:
        return
    if os.path.exists(INDEX_PATH):
        _rag_index = faiss.read_index(INDEX_PATH)
    if os.path.exists(META_PATH):
        with open(META_PATH, "r", encoding="utf-8") as f:
            _rag_texts = json.load(f)


def auto_segment_lead(lead: Dict[str, Any]) -> str:
    """Simple heuristic-based lead segmentation."""
    price = lead.get("final_price", 0)
    if price >= 1_000_000:
        return "VIP"
    if price >= 500_000:
        return "Premium"
    return "Standard"


def generate_followup_questions(lead: Dict[str, Any], k: int = 3) -> List[str]:
    """Suggest follow-up questions based on missing fields."""
    questions: List[str] = []
    answers = lead.get("answers_details", {}) or {}
    if "budget" not in answers:
        questions.append("Каков ваш целевой бюджет?")
    if "timeline" not in answers:
        questions.append("В какие сроки планируете запуск?")
    if "needs" not in answers:
        questions.append("Какие основные потребности у вашего бизнеса?")
    return questions[:k]


def predict_ltv(lead: Dict[str, Any]) -> float:
    """Very naive LTV prediction based on final price."""
    price = lead.get("final_price", 0)
    return round(price * 3.5, 2)


# initialize RAG index on import
load_rag_index()
