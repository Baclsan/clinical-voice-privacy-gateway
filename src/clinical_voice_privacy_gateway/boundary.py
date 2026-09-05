"""The only place that converts local artifacts into egress payloads."""

from __future__ import annotations

from .errors import BoundaryError
from .routing import Route
from .types import EgressPayload, RawTranscript, VerifiedSafeText


class DisclosureBoundary:
    """Route-specific egress authorization.

    NORMAL and CLINICAL are deliberately separate methods. Clinical egress has
    no API that accepts a RawTranscript.
    """

    def authorize_normal(self, raw: RawTranscript) -> EgressPayload:
        if not isinstance(raw, RawTranscript):
            raise BoundaryError("normal egress requires RawTranscript")
        return EgressPayload(raw.text, raw.sha256, Route.NORMAL.value, "raw")

    def authorize_clinical(self, safe: VerifiedSafeText) -> EgressPayload:
        if not isinstance(safe, VerifiedSafeText) or not safe._is_authentic():
            raise BoundaryError("clinical egress requires authentic VerifiedSafeText")
        return EgressPayload(safe.text, safe.sha256, Route.CLINICAL.value, "verified_safe")
