import pytest

from clinical_voice_privacy_gateway import (
    DurableProviderSink,
    FileHandoffJournal,
    PrivacyGateway,
    RawTranscript,
    RegexPrivacyVerifier,
)
from helpers import RecordingSink, SyntheticTransform


def test_durable_sink_requires_explicit_stable_idempotency_key(tmp_path):
    durable = DurableProviderSink(RecordingSink(), FileHandoffJournal(tmp_path / "journal"))
    gateway = PrivacyGateway(transform=SyntheticTransform(), verifier=RegexPrivacyVerifier(), sink=durable)
    raw = RawTranscript.from_text("normal text")

    with pytest.raises(ValueError, match="explicit stable idempotency key"):
        gateway.process(route="normal", raw=raw)
