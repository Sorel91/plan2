from __future__ import annotations

from dataclasses import dataclass

from g2p_modern.core.adapters import LegacyDatasetAdapter
from g2p_modern.core.retrieval import BoundaryRetriever
from g2p_modern.core.schemas import (
    GenerateRequest,
    GenerateResponse,
    PlanCandidate,
    RetrieveRequest,
    RetrieveResponse,
)


@dataclass(slots=True)
class PipelineConfig:
    model_path: str = "models/latest.pt"
    retrieval_index_path: str = "artifacts/retrieval.index"
    legacy_train_data_path: str = "Interface/static/Data/data_train_converted.pkl"


class GenerationPipeline:
    """Pipeline moderne: retrieval -> transfer -> generate -> post-process."""

    def __init__(self, config: PipelineConfig | None = None) -> None:
        self.config = config or PipelineConfig()
        self.samples = LegacyDatasetAdapter(self.config.legacy_train_data_path).load()
        self.retriever = BoundaryRetriever(self.samples)

    def retrieve(self, payload: RetrieveRequest) -> RetrieveResponse:
        query_boundary = [(point.x, point.y) for point in payload.boundary.points]
        hits = self.retriever.retrieve(query_boundary, k=payload.k)
        return RetrieveResponse(
            candidates=[PlanCandidate(name=item.name, score=item.score) for item in hits],
            meta={"status": "ok", "num_loaded_samples": len(self.samples)},
        )

    def generate(self, payload: GenerateRequest) -> GenerateResponse:
        return GenerateResponse(
            rooms=[],
            edges=[],
            meta={
                "status": "stub",
                "message": "Pipeline moderne initialisé, migration legacy à implémenter.",
                "num_boundary_points": len(payload.boundary.points),
            },
        )
