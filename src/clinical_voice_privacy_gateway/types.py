"""Security-relevant value types.

`VerifiedSafeText` is minted only after a verifier passes. `EgressPayload` is
minted only by the disclosure boundary. These capabilities prevent accidental
API misuse inside one Python process; they are not a sandbox against malicious
code with module introspection access.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


_VERIFIED_SEAL = object()
_EGRESS_SEAL = object()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "strict")).hexdigest()


@dataclass(frozen=True)
class RawTranscript:
    text: str
    sha256: str

    @classmethod
    def from_text(cls, text: str) -> "RawTranscript":
        if not isinstance(text, str) or not text.strip() or "\x00" in text:
            raise ValueError("raw transcript must be non-empty UTF-8 text")
        text.encode("utf-8", "strict")
        return cls(text=text, sha256=sha256_text(text))


@dataclass(frozen=True)
class CandidateSafeText:
    text: str

    def __post_init__(self) -> None:
        if not isinstance(self.text, str) or not self.text.strip() or "\x00" in self.text:
            raise ValueError("safe-text candidate must be non-empty UTF-8 text")
        self.text.encode("utf-8", "strict")


@dataclass(frozen=True, init=False)
class VerifiedSafeText:
    text: str
    sha256: str
    _seal: object

    def __init__(self, *_: object, **__: object) -> None:
        raise TypeError("VerifiedSafeText can only be created by a passing verifier")

    @classmethod
    def _mint(cls, text: str, *, seal: object) -> "VerifiedSafeText":
        if seal is not _VERIFIED_SEAL:
            raise TypeError("invalid verification capability")
        instance = object.__new__(cls)
        object.__setattr__(instance, "text", text)
        object.__setattr__(instance, "sha256", sha256_text(text))
        object.__setattr__(instance, "_seal", seal)
        return instance

    def _is_authentic(self) -> bool:
        return self._seal is _VERIFIED_SEAL and self.sha256 == sha256_text(self.text)


@dataclass(frozen=True, init=False)
class EgressPayload:
    text: str
    sha256: str
    route: str
    payload_kind: str
    _seal: object

    def __init__(self, *_: object, **__: object) -> None:
        raise TypeError("EgressPayload can only be created by DisclosureBoundary")

    @classmethod
    def _mint(
        cls,
        *,
        text: str,
        sha256: str,
        route: str,
        payload_kind: str,
        seal: object,
    ) -> "EgressPayload":
        if seal is not _EGRESS_SEAL or sha256 != sha256_text(text):
            raise TypeError("invalid egress capability")
        instance = object.__new__(cls)
        object.__setattr__(instance, "text", text)
        object.__setattr__(instance, "sha256", sha256)
        object.__setattr__(instance, "route", route)
        object.__setattr__(instance, "payload_kind", payload_kind)
        object.__setattr__(instance, "_seal", seal)
        return instance

    def _is_authentic(self) -> bool:
        expected_kind = "raw" if self.route == "normal" else "verified_safe" if self.route == "clinical" else None
        return (
            self._seal is _EGRESS_SEAL
            and expected_kind == self.payload_kind
            and self.sha256 == sha256_text(self.text)
        )
