"""Provider-neutral local privacy transform interface."""

from __future__ import annotations

from typing import Protocol

from .types import CandidateSafeText, RawTranscript


class PrivacyTransform(Protocol):
    """A local transform. Implementations must not disclose RAW externally."""

    def transform(self, raw: RawTranscript) -> CandidateSafeText: ...
