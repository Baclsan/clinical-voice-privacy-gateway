from clinical_voice_privacy_gateway import CandidateSafeText, RawTranscript


def test_raw_and_candidate_are_distinct_security_types():
    raw = RawTranscript.from_text("text")
    candidate = CandidateSafeText("safe text")
    assert type(raw) is not type(candidate)
