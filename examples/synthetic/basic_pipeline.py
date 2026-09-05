"""Synthetic-only demonstration. No real clinical data."""

from dataclasses import dataclass, field

from clinical_voice_privacy_gateway import (
    CandidateSafeText,
    PrivacyGateway,
    RawTranscript,
    RegexPrivacyVerifier,
    Route,
    Submission,
)


class DemoTransform:
    def transform(self, raw):
        return CandidateSafeText(
            raw.text.replace("Jane Maria Smith", "[PERSON]")
            .replace("+1 (555) 010-2020", "[PHONE]")
        )


@dataclass
class DemoSink:
    received: list[str] = field(default_factory=list)

    def submit(self, payload, *, idempotency_key):
        self.received.append(payload.text)
        return Submission(idempotency_key)


sink = DemoSink()
gateway = PrivacyGateway(transform=DemoTransform(), verifier=RegexPrivacyVerifier(), sink=sink)
raw = RawTranscript.from_text("Patient: Jane Maria Smith, phone +1 (555) 010-2020, cough for three days.")
gateway.process(route=Route.CLINICAL, raw=raw, idempotency_key="synthetic-demo")
print(sink.received[0])
