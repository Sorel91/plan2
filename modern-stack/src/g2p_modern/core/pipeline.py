from __future__ import annotations

from dataclasses import dataclass

from g2p_modern.core.schemas import GenerateRequest, GenerateResponse


@dataclass(slots=True)
class PipelineConfig:
    model_path: str = "models/latest.pt"
    retrieval_index_path: str = "artifacts/retrieval.index"


class GenerationPipeline:
    """Pipeline moderne: retrieval -> transfer -> generate -> post-process.

    Cette classe sert de façade testable pour remplacer progressivement les scripts legacy.
    """

    def __init__(self, config: PipelineConfig | None = None) -> None:
        self.config = config or PipelineConfig()

    def generate(self, payload: GenerateRequest) -> GenerateResponse:
        # Placeholder volontaire: la logique legacy sera migrée itérativement.
        return GenerateResponse(
            rooms=[],
            edges=[],
            meta={
                "status": "stub",
                "message": "Pipeline moderne initialisé, migration legacy à implémenter.",
                "num_boundary_points": len(payload.boundary.points),
            },
        )
