from __future__ import annotations

from fastapi import FastAPI

from g2p_modern.core.pipeline import GenerationPipeline
from g2p_modern.core.schemas import GenerateRequest, GenerateResponse

app = FastAPI(title="Graph2Plan Modern API", version="0.1.0")
pipeline = GenerationPipeline()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/generate", response_model=GenerateResponse)
def generate(payload: GenerateRequest) -> GenerateResponse:
    return pipeline.generate(payload)
