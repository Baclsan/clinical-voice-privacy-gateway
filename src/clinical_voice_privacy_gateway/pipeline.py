"""Minimal local-first pipeline with fail-closed clinical egress."""

from __future__ import annotations

import uuid

from .boundary import DisclosureBoundary
from .errors import TransformError, VerificationError
from .provider import ProviderSink, Submission
from .routing import Route
from .transform import PrivacyTransform
from .types import RawTranscript
from .verifier import RegexPrivacyVerifier


class PrivacyGateway:
    def __init__(
        self,
        *,
        transform: PrivacyTransform,
        verifier: RegexPrivacyVerifier,
        sink: ProviderSink,
        boundary: DisclosureBoundary | None = None,
    ) -> None:
        self._transform = transform
        self._verifier = verifier
        self._sink = sink
        self._boundary = boundary or DisclosureBoundary()

    def process(
        self,
        *,
        route: Route | str,
        raw: RawTranscript,
        idempotency_key: str | None = None,
    ) -> Submission:
        selected = Route.parse(route)
        key = idempotency_key or str(uuid.uuid4())

        if selected is Route.NORMAL:
            payload = self._boundary.authorize_normal(raw)
            return self._sink.submit(payload, idempotency_key=key)

        try:
            candidate = self._transform.transform(raw)
        except Exception as exc:
            raise TransformError("local privacy transform failed") from exc

        try:
            decision = self._verifier.verify(raw, candidate)
        except Exception as exc:
            raise VerificationError("privacy verifier failed") from exc

        if not decision.passed or decision.safe is None:
            reason = decision.reasons[0] if decision.reasons else "VERIFICATION_FAILED"
            raise VerificationError(f"clinical candidate rejected: {reason}")

        payload = self._boundary.authorize_clinical(decision.safe)
        return self._sink.submit(payload, idempotency_key=key)
