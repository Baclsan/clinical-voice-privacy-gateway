"""The only place that converts local artifacts into egress payloads."""

from __future__ import annotations

from .errors import BoundaryError
from .routing import Route
from .types import EgressPayload, RawTranscript, VerifiedSafeText, _EGRESS_SEAL


class DisclosureBoundary:
    """Route-specific egress authorization.

    NORMAL and CLINICAL are deliberately separate methods. Clinical egress has
    no API that accepts a RawTranscript.
    """

    def authorize_normal(self, raw: RawTranscript) -> EgressPayload:
        if not isinstance(raw, RawTranscript):
            raise BoundaryError("normal egress requires RawTranscript")
        return EgressPayload._mint(
            text=raw.text,
            sha256=raw.sha256,
            route=Route.NORMAL.value,
            payload_kind="raw",
            seal=_EGRESS_SEAL,
        )

    def authorize_clinical(self, safe: VerifiedSafeText) -> EgressPayload:
        if not isinstance(safe, VerifiedSafeText) or not safe._is_authentic():
            raise BoundaryError("clinical egress requires authentic VerifiedSafeText")
        return EgressPayload._mint(
            text=safe.text,
            sha256=safe.sha256,
            route=Route.CLINICAL.value,
            payload_kind="verified_safe",
            seal=_EGRESS_SEAL,
        )
