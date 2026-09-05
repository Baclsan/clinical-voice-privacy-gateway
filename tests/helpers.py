from __future__ import annotations

from dataclasses import dataclass, field

from clinical_voice_privacy_gateway import CandidateSafeText, Submission


class SyntheticTransform:
    def transform(self, raw):
        text = raw.text
        replacements = {
            "Иванов Алексей Олегович": "[PERSON]",
            "+7 999 123-45-67": "[PHONE]",
            "12.03.1985": "[DOB]",
            "Jane Maria Smith": "[PERSON]",
            "+1 (555) 010-2020": "[PHONE]",
        }
        for source, replacement in replacements.items():
            text = text.replace(source, replacement)
        return CandidateSafeText(text)


class CrashingTransform:
    def transform(self, raw):
        raise RuntimeError("synthetic transform crash")


@dataclass
class RecordingSink:
    calls: list[tuple[object, str]] = field(default_factory=list)

    def submit(self, payload, *, idempotency_key):
        self.calls.append((payload, idempotency_key))
        return Submission(f"submission-{len(self.calls)}")
