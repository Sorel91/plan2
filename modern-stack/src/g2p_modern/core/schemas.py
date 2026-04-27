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


class PlanCandidate(BaseModel):
    name: str
    score: float


class RetrieveRequest(BaseModel):
    boundary: Boundary
    k: int = Field(default=5, ge=1, le=100)


class RetrieveResponse(BaseModel):
    candidates: list[PlanCandidate]
    meta: dict[str, Any]


class GenerateRequest(BaseModel):
    boundary: Boundary
    constraints: list[RoomConstraint] = Field(default_factory=list)


class GenerateResponse(BaseModel):
    rooms: list[dict[str, Any]]
    edges: list[tuple[int, int]]
    meta: dict[str, Any]
