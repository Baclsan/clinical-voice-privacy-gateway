# Changelog

All notable public code-state changes are documented here.

No tagged public release has been published yet. The version numbers below describe merged package code states.

## 0.2.0 — 2026-09-05

### Added

- Durable provider-neutral handoff journal.
- Stable idempotency-key reuse across restart.
- Explicit `PREPARED`, `IN_FLIGHT`, `ADMISSION_UNKNOWN`, and `ACCEPTED` states.
- Crash-window recovery tests proving repeated transport attempts can map to one idempotent remote admission.
- Boundary-minted `EgressPayload` capability.
- Tests preventing idempotency-key rebinding and accepted-work resubmission.
- Journal privacy rule: no transcript/egress text and no plaintext idempotency key.

### Validation

- 21 local tests passed before merge.
- GitHub Actions passed on Python 3.11, 3.12, and 3.13 before merge and on `main` after merge.
- Intentional accepted-work resubmission mutation was detected by the test suite.

## 0.1.0 — 2026-09-05

### Added

- Provider-neutral NORMAL and CLINICAL routing model.
- Distinct raw, candidate-safe, and verifier-minted verified-safe security types.
- Fail-closed disclosure boundary and provider sink protocol.
- Demonstration deterministic verifier using synthetic identifiers.
- Synthetic-only examples and privacy/security documentation.
- GitHub Actions test matrix for Python 3.11–3.13.

### Validation

- 13 local tests passed before merge.
- GitHub Actions passed on Python 3.11, 3.12, and 3.13.
- Intentional CLINICAL-RAW egress mutation was detected by the test suite.
