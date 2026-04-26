from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Point(BaseModel):
    x: float
    y: float


class Boundary(BaseModel):
    points: list[Point] = Field(min_length=3)


class RoomConstraint(BaseModel):
    room_type: str
    min_count: int = 0
    max_count: int | None = None


class GenerateRequest(BaseModel):
    boundary: Boundary
    constraints: list[RoomConstraint] = Field(default_factory=list)


class GenerateResponse(BaseModel):
    rooms: list[dict[str, Any]]
    edges: list[tuple[int, int]]
    meta: dict[str, Any]
