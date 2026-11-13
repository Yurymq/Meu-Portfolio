"""Comparação simples e explicável entre descrições de objetos."""

from __future__ import annotations

import re
import unicodedata
from typing import Any

STOPWORDS = {
    "a", "as", "o", "os", "um", "uma", "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas", "com", "sem", "por", "para", "perto",
    "foi", "e", "ou", "que", "meu", "minha", "seu", "sua", "item",
}


def _tokens(value: str) -> set[str]:
    normalized = unicodedata.normalize("NFKD", value.casefold())
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    words = re.findall(r"[a-z0-9]+", normalized)
    return {word for word in words if len(word) > 2 and word not in STOPWORDS}


def rank_candidates(
    keywords: list[str],
    category: str,
    candidates: list[dict[str, Any]],
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Ordena candidatos por categoria e sobreposição de palavras-chave.

    A pontuação é apenas um indicador heurístico (0 a 100), não uma
    probabilidade de correspondência.
    """
    query_terms = _tokens(" ".join(keywords))
    ranked: list[dict[str, Any]] = []

    for candidate in candidates:
        description = str(candidate.get("description", ""))
        candidate_category = str(candidate.get("category", ""))
        candidate_terms = _tokens(description)
        if not query_terms:
            overlap = 0.0
        else:
            overlap = len(query_terms & candidate_terms) / len(query_terms | candidate_terms)

        category_match = bool(category) and category.casefold() == candidate_category.casefold()
        score = round(min(100.0, (overlap * 60) + (40 if category_match else 0)), 1)
        reasons = []
        if category_match:
            reasons.append("categoria compatível")
        shared = sorted(query_terms & candidate_terms)
        if shared:
            reasons.append("termos em comum: " + ", ".join(shared[:5]))

        ranked.append(
            {
                "id": candidate.get("id", ""),
                "description": description,
                "category": candidate_category,
                "score": score,
                "reason": "; ".join(reasons) if reasons else "poucos termos em comum",
            }
        )

    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[: max(0, limit)]
