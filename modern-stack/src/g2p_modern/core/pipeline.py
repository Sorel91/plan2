from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .layout_generator import generate_rect_rooms


@dataclass
class GenerateRequest:
    boundary: list[list[float]] | list[tuple[float, float]]
    constraints: list[Any] = field(default_factory=list)


@dataclass
class GenerateResponse:
    rooms: list[dict[str, Any]]
    edges: list[dict[str, str]]
    meta: dict[str, Any]


class GenerationPipeline:
    def generate(self, request: GenerateRequest) -> GenerateResponse:
        rooms = generate_rect_rooms(request.boundary, request.constraints)

        room_ids_by_type: dict[str, list[str]] = {}
        for room in rooms:
            room_ids_by_type.setdefault(room["room_type"], []).append(room["id"])

        edges: list[dict[str, str]] = []

        living_ids = room_ids_by_type.get("living", [])
        kitchen_ids = room_ids_by_type.get("kitchen", [])
        if living_ids and kitchen_ids:
            edges.append({"from": living_ids[0], "to": kitchen_ids[0]})

        bedroom_ids = room_ids_by_type.get("bedroom", [])
        bathroom_ids = room_ids_by_type.get("bathroom", [])
        if bathroom_ids:
            bathroom_id = bathroom_ids[0]
            for bedroom_id in bedroom_ids:
                edges.append({"from": bedroom_id, "to": bathroom_id})

        meta = {
            "status": "generated",
            "generator": "python_grid_v1",
            "num_rooms": len(rooms),
        }

        return GenerateResponse(rooms=rooms, edges=edges, meta=meta)
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
