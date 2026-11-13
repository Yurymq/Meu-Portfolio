from app.services.matching import rank_candidates


def test_rank_candidates_prioritizes_same_category_and_shared_terms():
    candidates = [
        {
            "id": "a",
            "description": "Estojo azul com canetas",
            "category": "Material escolar",
        },
        {
            "id": "b",
            "description": "Fone bluetooth preto",
            "category": "Eletrônico",
        },
    ]

    ranked = rank_candidates(
        keywords=["estojo", "azul", "canetas"],
        category="Material escolar",
        candidates=candidates,
    )

    assert ranked[0]["id"] == "a"
    assert ranked[0]["score"] > ranked[1]["score"]
    assert "categoria compatível" in ranked[0]["reason"]


def test_rank_candidates_returns_empty_for_no_candidates():
    assert rank_candidates(["mochila"], "Acessório", []) == []


def test_rank_candidates_respects_limit():
    candidates = [
        {"id": str(index), "description": "mochila preta", "category": "Acessório"}
        for index in range(6)
    ]
    ranked = rank_candidates(["mochila", "preta"], "Acessório", candidates, limit=3)
    assert len(ranked) == 3
