from clinical_voice_privacy_gateway import PrivacyGateway, RawTranscript, RegexPrivacyVerifier, Route

from helpers import RecordingSink, SyntheticTransform


def test_clinical_raw_never_reaches_sink_and_verified_safe_does():
    secret = "Пациент Иванов Алексей Олегович, телефон +7 999 123-45-67, жалобы на кашель."
    raw = RawTranscript.from_text(secret)
    sink = RecordingSink()
    gateway = PrivacyGateway(transform=SyntheticTransform(), verifier=RegexPrivacyVerifier(), sink=sink)

    gateway.process(route=Route.CLINICAL, raw=raw, idempotency_key="clinical-1")

    assert len(sink.calls) == 1
    payload, _ = sink.calls[0]
    assert payload.payload_kind == "verified_safe"
    assert payload.route == "clinical"
    assert "Иванов Алексей Олегович" not in payload.text
    assert "+7 999 123-45-67" not in payload.text
    assert "[PERSON]" in payload.text
    assert "[PHONE]" in payload.text
    assert secret not in [call[0].text for call in sink.calls]
