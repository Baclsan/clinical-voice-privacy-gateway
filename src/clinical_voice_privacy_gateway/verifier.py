"""Deterministic fail-closed verifier for synthetic/demo clinical identifiers.

This verifier is intentionally conservative and incomplete. It demonstrates the
security boundary; it is not a complete de-identification standard.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Pattern

from .types import CandidateSafeText, RawTranscript, VerifiedSafeText, _VERIFIED_SEAL


@dataclass(frozen=True)
class VerificationDecision:
    passed: bool
    reasons: tuple[str, ...]
    safe: VerifiedSafeText | None = None


_DEFAULT_PATTERNS: tuple[tuple[str, Pattern[str]], ...] = (
    ("EMAIL", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("PHONE", re.compile(r"(?<!\d)(?:\+?\d[\s().-]*)?(?:\d[\s().-]*){9,14}(?!\d)")),
    ("DOB", re.compile(r"(?i)\b(?:date of birth|dob|дата рождения)\s*[:=-]?\s*\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b")),
    ("LABELED_NAME_RU", re.compile(r"(?i)\b(?:пациент|пациентка|фио)\s*[:—-]?\s*[А-ЯЁ][а-яё'-]+(?:\s+[А-ЯЁ][а-яё'-]+){1,2}\b")),
    ("LABELED_NAME_EN", re.compile(r"(?i)\b(?:patient|name)\s*[:—-]?\s*[A-Z][A-Za-z'-]+(?:\s+[A-Z][A-Za-z'-]+){1,2}\b")),
)

_ALLOWED_PLACEHOLDERS = {
    "PERSON", "PHONE", "DOB", "EMAIL", "ADDRESS", "IDENTIFIER"
}


class RegexPrivacyVerifier:
    def __init__(self, patterns: tuple[tuple[str, Pattern[str]], ...] = _DEFAULT_PATTERNS) -> None:
        self._patterns = patterns

    def verify(self, raw: RawTranscript, candidate: CandidateSafeText) -> VerificationDecision:
        reasons: set[str] = set()
        text = candidate.text

        if text.strip() == raw.text.strip():
            reasons.add("RAW_ECHO")
        if len(text.encode("utf-8")) > max(4096, 4 * len(raw.text.encode("utf-8"))):
            reasons.add("OUTPUT_EXPANSION")
        if len(text.encode("utf-8")) < max(1, len(raw.text.encode("utf-8")) // 4):
            reasons.add("OUTPUT_TRUNCATED")
        if "```" in text or any(ord(ch) < 32 and ch not in "\n\t" for ch in text):
            reasons.add("OUTPUT_SCHEMA")

        placeholders = set(re.findall(r"\[([A-Z_]{2,32})\]", text))
        if placeholders - _ALLOWED_PLACEHOLDERS:
            reasons.add("OUTPUT_SCHEMA")

        for code, pattern in self._patterns:
            if pattern.search(text):
                reasons.add(f"RESIDUAL_{code}")

        if reasons:
            return VerificationDecision(False, tuple(sorted(reasons)), None)
        safe = VerifiedSafeText._mint(text, seal=_VERIFIED_SEAL)
        return VerificationDecision(True, (), safe)
