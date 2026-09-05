import pytest

from clinical_voice_privacy_gateway import (
    CandidateSafeText,
    PrivacyGateway,
    RawTranscript,
    RegexPrivacyVerifier,
    RouteError,
    TransformError,
    VerificationError,
)

from helpers import CrashingTransform, RecordingSink, SyntheticTransform


class EchoTransform:
    def transform(self, raw):
        return CandidateSafeText(raw.text)


class CrashingVerifier:
    def verify(self, raw, candidate):
        raise RuntimeError("synthetic verifier crash")


def test_transform_failure_causes_zero_sink_calls():
    sink = RecordingSink()
    gateway = PrivacyGateway(transform=CrashingTransform(), verifier=RegexPrivacyVerifier(), sink=sink)
    raw = RawTranscript.from_text("Пациент Иванов Алексей Олегович, жалобы на кашель.")

    with pytest.raises(TransformError):
        gateway.process(route="clinical", raw=raw)

    assert sink.calls == []


def test_verifier_rejection_causes_zero_sink_calls():
    sink = RecordingSink()
    gateway = PrivacyGateway(transform=EchoTransform(), verifier=RegexPrivacyVerifier(), sink=sink)
    raw = RawTranscript.from_text("Пациент Иванов Алексей Олегович, жалобы на кашель.")

    with pytest.raises(VerificationError):
        gateway.process(route="clinical", raw=raw)

    assert sink.calls == []


def test_verifier_exception_causes_zero_sink_calls():
    sink = RecordingSink()
    gateway = PrivacyGateway(transform=SyntheticTransform(), verifier=CrashingVerifier(), sink=sink)
    raw = RawTranscript.from_text("Пациент Иванов Алексей Олегович, жалобы на кашель.")

    with pytest.raises(VerificationError):
        gateway.process(route="clinical", raw=raw)

    assert sink.calls == []


def test_unknown_route_fails_before_transform_or_sink():
    sink = RecordingSink()
    gateway = PrivacyGateway(transform=CrashingTransform(), verifier=RegexPrivacyVerifier(), sink=sink)
    raw = RawTranscript.from_text("text")

    with pytest.raises(RouteError):
        gateway.process(route="maybe-clinical", raw=raw)

    assert sink.calls == []
