from __future__ import annotations

from fastapi import FastAPI

from g2p_modern.core.pipeline import GenerationPipeline
from g2p_modern.core.schemas import (
    GenerateRequest,
    GenerateResponse,
    RetrieveRequest,
    RetrieveResponse,
)

app = FastAPI(title="Graph2Plan Modern API", version="0.2.0")
pipeline = GenerationPipeline()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/retrieve", response_model=RetrieveResponse)
def retrieve(payload: RetrieveRequest) -> RetrieveResponse:
    return pipeline.retrieve(payload)


@app.post("/v1/generate", response_model=GenerateResponse)
def generate(payload: GenerateRequest) -> GenerateResponse:
    return pipeline.generate(payload)
