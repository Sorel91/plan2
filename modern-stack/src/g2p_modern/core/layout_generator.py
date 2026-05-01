from __future__ import annotations

from math import ceil, sqrt
from typing import Any


def _get_constraint_value(constraint: Any, key: str, default: Any = None) -> Any:
    if isinstance(constraint, dict):
        return constraint.get(key, default)
    return getattr(constraint, key, default)


def _iter_room_targets(constraints: list[Any]) -> list[tuple[str, int]]:
    room_targets: list[tuple[str, int]] = []
    for constraint in constraints or []:
        room_type = _get_constraint_value(constraint, "room_type")
        min_count = _get_constraint_value(constraint, "min_count", 0) or 0
        if room_type and min_count > 0:
            room_targets.append((room_type, int(min_count)))
    return room_targets


def generate_rect_rooms(boundary: list[list[float]] | list[tuple[float, float]], constraints: list[Any]) -> list[dict[str, Any]]:
    if not boundary:
        return []

    xs = [float(p[0]) for p in boundary]
    ys = [float(p[1]) for p in boundary]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    total_width = max_x - min_x
    total_height = max_y - min_y
    if total_width <= 0 or total_height <= 0:
        return []

    room_targets = _iter_room_targets(constraints)
    room_types: list[str] = []
    for room_type, count in room_targets:
        room_types.extend([room_type] * count)

    if not room_types:
        room_types = ["living", "kitchen", "bedroom", "bathroom"]

    room_count = len(room_types)
    cols = ceil(sqrt(room_count))
    rows = ceil(room_count / cols)

    room_width = total_width / cols
    room_height = total_height / rows

    rooms: list[dict[str, Any]] = []
    for idx, room_type in enumerate(room_types):
        row = idx // cols
        col = idx % cols
        x = min_x + col * room_width
        y = min_y + row * room_height
        area = room_width * room_height
        rooms.append(
            {
                "id": f"room_{idx + 1}",
                "room_type": room_type,
                "x": x,
                "y": y,
                "width": room_width,
                "height": room_height,
                "area": area,
            }
        )

    return rooms
