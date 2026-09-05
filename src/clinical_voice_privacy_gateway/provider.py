"""Provider-neutral sink interface."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .types import EgressPayload


@dataclass(frozen=True)
class Submission:
    submission_id: str


class ProviderSink(Protocol):
    def submit(self, payload: EgressPayload, *, idempotency_key: str) -> Submission: ...
