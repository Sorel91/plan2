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
