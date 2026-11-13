"""Integração com um modelo de linguagem para estruturar descrições."""

from __future__ import annotations

import json
import os
import re
from typing import Any


ALLOWED_CATEGORIES = {
    "Eletrônico",
    "Documento",
    "Acessório",
    "Roupa",
    "Material escolar",
    "Chave/Carteira",
    "Outro",
}

INSTRUCTIONS = """
Você organiza descrições de objetos perdidos e encontrados.
Analise somente as informações fornecidas. Não invente marca, local, dono,
valor ou características que não foram mencionadas.
Responda SOMENTE com um objeto JSON válido contendo:
- category: exatamente uma destas opções: Eletrônico, Documento, Acessório,
  Roupa, Material escolar, Chave/Carteira, Outro.
- normalized_description: uma frase curta e fiel ao texto original.
- keywords: lista de 3 a 8 palavras-chave úteis, sem duplicatas.
Se faltarem detalhes, não faça suposições. Não inclua markdown nem comentários.
""".strip()


def analyze_description(description: str) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não está configurada no arquivo .env.")

    model = os.getenv("OPENAI_MODEL", "gpt-6-astra").strip() or "gpt-6-astra"
    # Importação local permite iniciar a API e usar /api/health sem a SDK instalada.
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        instructions=INSTRUCTIONS,
        input=f"Descrição recebida:\n{description}",
    )

    raw_output = (response.output_text or "").strip()
    raw_output = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_output, flags=re.IGNORECASE)
    try:
        result = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        raise ValueError("O modelo retornou um formato inesperado. Tente novamente.") from exc

    if not isinstance(result, dict):
        raise ValueError("A resposta do modelo não é um objeto JSON.")

    category = result.get("category")
    normalized = result.get("normalized_description")
    keywords = result.get("keywords")
    if category not in ALLOWED_CATEGORIES:
        raise ValueError("A categoria retornada não é válida.")
    if not isinstance(normalized, str) or not normalized.strip():
        raise ValueError("A descrição padronizada não foi retornada.")
    if not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords):
        raise ValueError("As palavras-chave retornadas não são válidas.")

    return {
        "category": category,
        "normalized_description": normalized.strip(),
        "keywords": [item.strip() for item in keywords if item.strip()][:8],
    }
