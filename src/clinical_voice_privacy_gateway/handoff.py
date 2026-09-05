"""Durable, provider-neutral idempotent handoff.

The journal persists only egress metadata and hashes; it never stores payload text.
A stable idempotency key must be supplied by the caller for restart-safe retries.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from .errors import HandoffError, HandoffStateError, HandoffUncertainError
from .provider import ProviderSink, Submission
from .types import EgressPayload


class HandoffState(str, Enum):
    PREPARED = "prepared"
    IN_FLIGHT = "in_flight"
    ADMISSION_UNKNOWN = "admission_unknown"
    ACCEPTED = "accepted"


@dataclass(frozen=True)
class HandoffRecord:
    version: int
    idempotency_key_sha256: str
    route: str
    payload_kind: str
    payload_sha256: str
    state: str
    attempts: int
    submission_id: str | None = None

    def validated(self) -> "HandoffRecord":
        if self.version != 1:
            raise HandoffStateError("unsupported handoff record version")
        if len(self.idempotency_key_sha256) != 64 or any(ch not in "0123456789abcdef" for ch in self.idempotency_key_sha256):
            raise HandoffStateError("invalid persisted idempotency key digest")
        if self.route not in {"normal", "clinical"}:
            raise HandoffStateError("invalid persisted route")
        expected_kind = "raw" if self.route == "normal" else "verified_safe"
        if self.payload_kind != expected_kind:
            raise HandoffStateError("persisted route/payload kind mismatch")
        if len(self.payload_sha256) != 64 or any(ch not in "0123456789abcdef" for ch in self.payload_sha256):
            raise HandoffStateError("invalid persisted payload digest")
        if self.state not in {state.value for state in HandoffState}:
            raise HandoffStateError("invalid persisted handoff state")
        if not isinstance(self.attempts, int) or self.attempts < 0:
            raise HandoffStateError("invalid persisted attempt count")
        if self.state == HandoffState.ACCEPTED.value:
            if not isinstance(self.submission_id, str) or not self.submission_id.strip():
                raise HandoffStateError("accepted handoff has no submission id")
        elif self.submission_id is not None:
            raise HandoffStateError("non-accepted handoff must not contain a submission id")
        return self


def _valid_key(value: Any) -> bool:
    return isinstance(value, str) and 1 <= len(value) <= 256 and "\x00" not in value


def _key_digest(idempotency_key: str) -> str:
    return hashlib.sha256(idempotency_key.encode("utf-8", "strict")).hexdigest()


def _record_name_from_digest(digest: str) -> str:
    return digest + ".json"


class FileHandoffJournal:
    """Small atomic JSON journal for one record per idempotency key.

    This v0.2 implementation provides crash/restart durability, not cross-process
    mutual exclusion. Use one writer per idempotency key.
    """

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        try:
            self.root.chmod(0o700)
        except OSError:
            pass

    def load(self, idempotency_key: str) -> HandoffRecord | None:
        if not _valid_key(idempotency_key):
            raise ValueError("idempotency key must be bounded non-empty text")
        digest = _key_digest(idempotency_key)
        path = self.root / _record_name_from_digest(digest)
        if not path.exists():
            return None
        try:
            raw = path.read_bytes()
            if not 0 < len(raw) <= 64 * 1024:
                raise ValueError
            value = json.loads(raw.decode("utf-8", "strict"))
            if not isinstance(value, dict):
                raise ValueError
            record = HandoffRecord(**value).validated()
        except (OSError, UnicodeError, TypeError, ValueError):
            raise HandoffStateError("handoff journal record is unreadable or invalid") from None
        if record.idempotency_key_sha256 != digest:
            raise HandoffStateError("handoff journal key mismatch")
        return record

    def save(self, record: HandoffRecord) -> None:
        record.validated()
        path = self.root / _record_name_from_digest(record.idempotency_key_sha256)
        payload = (json.dumps(asdict(record), sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
        descriptor, temporary_name = tempfile.mkstemp(prefix=".handoff-", suffix=".tmp", dir=self.root)
        temporary = Path(temporary_name)
        try:
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "wb", closefd=True) as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
            try:
                directory_fd = os.open(self.root, os.O_RDONLY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
            except OSError:
                pass
        finally:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass


class DurableProviderSink:
    """Wrap a provider sink with durable idempotency state.

    The underlying provider MUST deduplicate repeated submissions carrying the
    same idempotency key. That contract closes the crash window where admission
    succeeds remotely but the local ACCEPTED record is not yet durable.
    """

    requires_explicit_idempotency_key = True

    def __init__(self, sink: ProviderSink, journal: FileHandoffJournal) -> None:
        self._sink = sink
        self._journal = journal

    def submit(self, payload: EgressPayload, *, idempotency_key: str) -> Submission:
        if not _valid_key(idempotency_key):
            raise ValueError("durable handoff requires a bounded stable idempotency key")
        if not isinstance(payload, EgressPayload) or not payload._is_authentic():
            raise HandoffStateError("durable handoff requires a boundary-authorized payload")

        record = self._prepare(payload, idempotency_key)
        if record.state == HandoffState.ACCEPTED.value:
            return Submission(record.submission_id or "")

        attempt = HandoffRecord(
            version=1,
            idempotency_key_sha256=record.idempotency_key_sha256,
            route=record.route,
            payload_kind=record.payload_kind,
            payload_sha256=record.payload_sha256,
            state=HandoffState.IN_FLIGHT.value,
            attempts=record.attempts + 1,
        )
        self._journal.save(attempt)

        try:
            submission = self._sink.submit(payload, idempotency_key=idempotency_key)
        except Exception as exc:
            uncertain = HandoffRecord(
                version=1,
                idempotency_key_sha256=attempt.idempotency_key_sha256,
                route=attempt.route,
                payload_kind=attempt.payload_kind,
                payload_sha256=attempt.payload_sha256,
                state=HandoffState.ADMISSION_UNKNOWN.value,
                attempts=attempt.attempts,
            )
            self._journal.save(uncertain)
            raise HandoffUncertainError("provider admission is unknown; retry only with the same idempotency key") from exc

        if not isinstance(submission, Submission) or not isinstance(submission.submission_id, str) or not submission.submission_id.strip():
            uncertain = HandoffRecord(
                version=1,
                idempotency_key_sha256=attempt.idempotency_key_sha256,
                route=attempt.route,
                payload_kind=attempt.payload_kind,
                payload_sha256=attempt.payload_sha256,
                state=HandoffState.ADMISSION_UNKNOWN.value,
                attempts=attempt.attempts,
            )
            self._journal.save(uncertain)
            raise HandoffUncertainError("provider returned an invalid admission result")

        accepted = HandoffRecord(
            version=1,
            idempotency_key_sha256=attempt.idempotency_key_sha256,
            route=attempt.route,
            payload_kind=attempt.payload_kind,
            payload_sha256=attempt.payload_sha256,
            state=HandoffState.ACCEPTED.value,
            attempts=attempt.attempts,
            submission_id=submission.submission_id,
        )
        self._journal.save(accepted)
        return submission

    def _prepare(self, payload: EgressPayload, idempotency_key: str) -> HandoffRecord:
        existing = self._journal.load(idempotency_key)
        if existing is not None:
            if (
                existing.route != payload.route
                or existing.payload_kind != payload.payload_kind
                or existing.payload_sha256 != payload.sha256
            ):
                raise HandoffStateError("idempotency key is already bound to a different payload")
            return existing

        record = HandoffRecord(
            version=1,
            idempotency_key_sha256=_key_digest(idempotency_key),
            route=payload.route,
            payload_kind=payload.payload_kind,
            payload_sha256=payload.sha256,
            state=HandoffState.PREPARED.value,
            attempts=0,
        )
        self._journal.save(record)
        return record


__all__ = [
    "DurableProviderSink",
    "FileHandoffJournal",
    "HandoffRecord",
    "HandoffState",
]
