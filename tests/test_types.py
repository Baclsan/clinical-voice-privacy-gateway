from clinical_voice_privacy_gateway import CandidateSafeText, RawTranscript


def test_raw_and_candidate_are_distinct_security_types():
    raw = RawTranscript.from_text("text")
    candidate = CandidateSafeText("safe text")
    assert type(raw) is not type(candidate)


def test_egress_payload_cannot_be_constructed_directly():
    from clinical_voice_privacy_gateway import EgressPayload
    import pytest

    with pytest.raises(TypeError):
        EgressPayload("text", "digest", "clinical", "verified_safe")
