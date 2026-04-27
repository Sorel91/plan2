from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import pickle


@dataclass(slots=True)
class LegacySample:
    name: str
    boundary: list[tuple[float, float]]
    raw: Any


def _normalize_boundary(boundary_raw: Any) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for item in boundary_raw:
        # legacy format often contains x,y,dir,isNew
        if len(item) >= 2:
            points.append((float(item[0]), float(item[1])))
    return points


class LegacyDatasetAdapter:
    """Reads legacy `.pkl` files and maps them to a small typed contract."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> list[LegacySample]:
        if not self.path.exists():
            return []

        payload = pickle.load(self.path.open("rb"))
        data = payload.get("data", [])
        name_list = payload.get("nameList") or payload.get("trainNameList") or []

        result: list[LegacySample] = []
        for idx, item in enumerate(data):
            name = str(name_list[idx]) if idx < len(name_list) else f"sample_{idx}"
            boundary_raw = getattr(item, "boundary", [])
            result.append(
                LegacySample(
                    name=name,
                    boundary=_normalize_boundary(boundary_raw),
                    raw=item,
                )
            )
        return result
