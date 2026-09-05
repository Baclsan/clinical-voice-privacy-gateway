"""Explicit route selection before disclosure decisions."""

from __future__ import annotations

from enum import Enum

from .errors import RouteError


class Route(str, Enum):
    NORMAL = "normal"
    CLINICAL = "clinical"

    @classmethod
    def parse(cls, value: "Route | str") -> "Route":
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            try:
                return cls(value.strip().lower())
            except ValueError:
                pass
        raise RouteError("route is missing or unsupported")
