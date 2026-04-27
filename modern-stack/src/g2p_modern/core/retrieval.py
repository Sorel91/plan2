from __future__ import annotations

from dataclasses import dataclass
import math

from g2p_modern.core.adapters import LegacySample


@dataclass(slots=True)
class RetrievalResult:
    name: str
    score: float


def _boundary_signature(points: list[tuple[float, float]]) -> tuple[float, float, float]:
    if not points:
        return (0.0, 0.0, 0.0)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    area_proxy = max(xs) - min(xs)
    area_proxy *= max(ys) - min(ys)
    return (cx, cy, area_proxy)


class BoundaryRetriever:
    def __init__(self, samples: list[LegacySample]) -> None:
        self.samples = samples

    def retrieve(self, boundary: list[tuple[float, float]], k: int = 5) -> list[RetrievalResult]:
        qx, qy, qa = _boundary_signature(boundary)
        scored: list[RetrievalResult] = []
        for sample in self.samples:
            sx, sy, sa = _boundary_signature(sample.boundary)
            dist = math.sqrt((qx - sx) ** 2 + (qy - sy) ** 2 + ((qa - sa) / 1000.0) ** 2)
            scored.append(RetrievalResult(name=sample.name, score=dist))
        scored.sort(key=lambda item: item.score)
        return scored[: max(k, 0)]
