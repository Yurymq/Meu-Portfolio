from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.services.ai_service import analyze_description
from app.services.matching import rank_candidates

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(
    title="Assistente IA para Achados e Perdidos",
    description="Protótipo de classificação de descrições e sugestão de possíveis correspondências.",
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "../static"), name="static")


class CandidateItem(BaseModel):
    id: str = Field(default="", max_length=80)
    description: str = Field(min_length=3, max_length=500)
    category: str = Field(default="Outro", max_length=40)


class AnalyzeRequest(BaseModel):
    description: str = Field(min_length=12, max_length=1000)
    candidate_items: list[CandidateItem] = Field(default_factory=list, max_length=50)


@app.get("/")
def home() -> FileResponse:
    return FileResponse(BASE_DIR / "../static/index.html")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ai-found-and-lost"}


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest) -> dict[str, Any]:
    try:
        analysis = analyze_description(request.description)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:  # Não expõe credenciais ou detalhes do provedor ao cliente.
        logger.exception("Falha ao consultar o serviço de IA")
        raise HTTPException(
            status_code=502,
            detail="Não foi possível concluir a análise. Verifique o modelo e a configuração da API.",
        ) from exc

    matches = rank_candidates(
        keywords=analysis["keywords"],
        category=analysis["category"],
        candidates=[item.model_dump() for item in request.candidate_items],
    )
    return {**analysis, "matches": matches}
