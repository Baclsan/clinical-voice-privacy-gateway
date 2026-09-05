from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from clinical_voice_privacy_gateway import (
    CandidateSafeText,
    DisclosureBoundary,
    DurableProviderSink,
    FileHandoffJournal,
    HandoffState,
    HandoffStateError,
    HandoffUncertainError,
    RawTranscript,
    RegexPrivacyVerifier,
    Submission,
)


def clinical_payload(text: str = "Пациент [PERSON], жалобы на кашель."):
    raw = RawTranscript.from_text("Пациент Иванов Алексей Олегович, жалобы на кашель.")
    decision = RegexPrivacyVerifier().verify(raw, CandidateSafeText(text))
    assert decision.passed and decision.safe is not None
    return DisclosureBoundary().authorize_clinical(decision.safe)


@dataclass
class IdempotentFakeProvider:
    by_key: dict[str, Submission] = field(default_factory=dict)
    attempts: list[str] = field(default_factory=list)
    admissions: int = 0
    admit_then_timeout_once: bool = False

    def submit(self, payload, *, idempotency_key):
        self.attempts.append(idempotency_key)
        if idempotency_key in self.by_key:
            return self.by_key[idempotency_key]
        submission = Submission(f"submission-{len(self.by_key) + 1}")
        self.by_key[idempotency_key] = submission
        self.admissions += 1
        if self.admit_then_timeout_once:
            self.admit_then_timeout_once = False
            raise TimeoutError("synthetic timeout after remote admission")
        return submission


class MustNotSubmit:
    def submit(self, payload, *, idempotency_key):
        raise AssertionError("accepted durable handoff must not resubmit")


class SimulatedCrash(BaseException):
    pass


class CrashBeforeAcceptedJournal(FileHandoffJournal):
    def __init__(self, root):
        super().__init__(root)
        self._crash = True

    def save(self, record):
        if self._crash and record.state == HandoffState.ACCEPTED.value:
            self._crash = False
            raise SimulatedCrash("synthetic crash after provider admission")
        super().save(record)


def test_prepare_is_durable_before_provider_call(tmp_path):
    provider = IdempotentFakeProvider()
    journal = FileHandoffJournal(tmp_path / "journal")
    durable = DurableProviderSink(provider, journal)
    payload = clinical_payload()

    result = durable.submit(payload, idempotency_key="job-001")

    assert result.submission_id == "submission-1"
    record = journal.load("job-001")
    assert record is not None
    assert record.state == HandoffState.ACCEPTED.value
    assert record.attempts == 1
    assert record.payload_sha256 == payload.sha256


def test_accepted_restart_returns_record_without_resubmit(tmp_path):
    root = tmp_path / "journal"
    payload = clinical_payload()
    first_provider = IdempotentFakeProvider()
    first = DurableProviderSink(first_provider, FileHandoffJournal(root))
    accepted = first.submit(payload, idempotency_key="job-accepted")

    restarted = DurableProviderSink(MustNotSubmit(), FileHandoffJournal(root))
    again = restarted.submit(payload, idempotency_key="job-accepted")

    assert again == accepted
    assert first_provider.admissions == 1


def test_admission_unknown_restart_reuses_same_key_without_duplicate_admission(tmp_path):
    root = tmp_path / "journal"
    payload = clinical_payload()
    provider = IdempotentFakeProvider(admit_then_timeout_once=True)
    first = DurableProviderSink(provider, FileHandoffJournal(root))

    with pytest.raises(HandoffUncertainError):
        first.submit(payload, idempotency_key="job-uncertain")

    uncertain = FileHandoffJournal(root).load("job-uncertain")
    assert uncertain is not None
    assert uncertain.state == HandoffState.ADMISSION_UNKNOWN.value

    restarted = DurableProviderSink(provider, FileHandoffJournal(root))
    result = restarted.submit(payload, idempotency_key="job-uncertain")

    assert result.submission_id == "submission-1"
    assert provider.attempts == ["job-uncertain", "job-uncertain"]
    assert provider.admissions == 1
    assert FileHandoffJournal(root).load("job-uncertain").state == HandoffState.ACCEPTED.value


def test_crash_after_remote_admission_before_local_accept_recovers_with_same_key(tmp_path):
    root = tmp_path / "journal"
    payload = clinical_payload()
    provider = IdempotentFakeProvider()
    crashing = DurableProviderSink(provider, CrashBeforeAcceptedJournal(root))

    with pytest.raises(SimulatedCrash):
        crashing.submit(payload, idempotency_key="job-crash-window")

    stranded = FileHandoffJournal(root).load("job-crash-window")
    assert stranded is not None
    assert stranded.state == HandoffState.IN_FLIGHT.value
    assert provider.admissions == 1

    restarted = DurableProviderSink(provider, FileHandoffJournal(root))
    result = restarted.submit(payload, idempotency_key="job-crash-window")

    assert result.submission_id == "submission-1"
    assert provider.attempts == ["job-crash-window", "job-crash-window"]
    assert provider.admissions == 1
    recovered = FileHandoffJournal(root).load("job-crash-window")
    assert recovered.state == HandoffState.ACCEPTED.value
    assert recovered.attempts == 2


def test_same_idempotency_key_cannot_be_rebound_to_different_payload(tmp_path):
    root = tmp_path / "journal"
    provider = IdempotentFakeProvider()
    durable = DurableProviderSink(provider, FileHandoffJournal(root))
    first = clinical_payload("Пациент [PERSON], жалобы на кашель.")
    durable.submit(first, idempotency_key="job-bound")

    raw = RawTranscript.from_text("normal unrelated text")
    different = DisclosureBoundary().authorize_normal(raw)
    with pytest.raises(HandoffStateError):
        durable.submit(different, idempotency_key="job-bound")

    assert provider.admissions == 1


def test_journal_does_not_persist_payload_text(tmp_path):
    root = tmp_path / "journal"
    provider = IdempotentFakeProvider()
    durable = DurableProviderSink(provider, FileHandoffJournal(root))
    payload = clinical_payload("Пациент [PERSON], кодовое слово SYNTHETIC-CONTENT-XYZ.")

    durable.submit(payload, idempotency_key="job-no-text")

    combined = b"".join(path.read_bytes() for path in root.glob("*.json"))
    assert b"SYNTHETIC-CONTENT-XYZ" not in combined
    assert b"job-no-text" not in combined
    assert payload.sha256.encode() in combined
