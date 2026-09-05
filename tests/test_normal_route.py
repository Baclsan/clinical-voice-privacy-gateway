from clinical_voice_privacy_gateway import PrivacyGateway, RawTranscript, RegexPrivacyVerifier, Route

from helpers import RecordingSink, SyntheticTransform


def test_normal_raw_is_explicitly_allowed_to_sink():
    raw = RawTranscript.from_text("ordinary non-clinical note")
    sink = RecordingSink()
    gateway = PrivacyGateway(transform=SyntheticTransform(), verifier=RegexPrivacyVerifier(), sink=sink)

    gateway.process(route=Route.NORMAL, raw=raw, idempotency_key="normal-1")

    assert len(sink.calls) == 1
    payload, key = sink.calls[0]
    assert payload.text == raw.text
    assert payload.payload_kind == "raw"
    assert payload.route == "normal"
    assert key == "normal-1"
