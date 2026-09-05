import pytest

from clinical_voice_privacy_gateway import (
    BoundaryError,
    CandidateSafeText,
    DisclosureBoundary,
    RawTranscript,
    RegexPrivacyVerifier,
    VerifiedSafeText,
)


def test_verified_safe_text_cannot_be_constructed_directly():
    with pytest.raises(TypeError):
        VerifiedSafeText("pretend safe")


def test_clinical_boundary_rejects_raw_transcript():
    boundary = DisclosureBoundary()
    raw = RawTranscript.from_text("raw clinical transcript")

    with pytest.raises(BoundaryError):
        boundary.authorize_clinical(raw)  # type: ignore[arg-type]


def test_clinical_boundary_accepts_only_verifier_minted_safe_text():
    raw = RawTranscript.from_text("Пациент Иванов Алексей Олегович, жалобы на кашель.")
    candidate = CandidateSafeText("Пациент [PERSON], жалобы на кашель.")
    decision = RegexPrivacyVerifier().verify(raw, candidate)

    assert decision.passed
    payload = DisclosureBoundary().authorize_clinical(decision.safe)
    assert payload.payload_kind == "verified_safe"
    assert payload.text == candidate.text
