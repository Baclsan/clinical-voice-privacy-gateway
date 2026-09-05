# Clinical Voice Privacy Gateway

Local-first privacy boundary primitives for clinical voice AI workflows.

The core rule is deliberately asymmetric:

- **NORMAL** traffic may send a raw transcript to an external provider.
- **CLINICAL** traffic must keep raw transcript text local. Only deterministic-verifier-approved `VerifiedSafeText` may cross the disclosure boundary.

## Minimal architecture

```text
voice/audio -> local STT -> explicit route

NORMAL   -> RawTranscript ---------------------> DisclosureBoundary -> ProviderSink
CLINICAL -> RawTranscript -> local transform
                           -> candidate
                           -> deterministic verifier
                           -> VerifiedSafeText -> DisclosureBoundary -> ProviderSink
```

Unknown routes and transform/verifier failures fail closed before any provider call.

## Why separate security types?

`RawTranscript`, `CandidateSafeText`, and `VerifiedSafeText` are intentionally distinct. `VerifiedSafeText` cannot be directly constructed by normal callers; it is minted by a passing verifier. NORMAL raw text is never mislabeled as verified-safe clinical text.

## Test the invariant

```bash
python -m pip install -e '.[test]'
python -m pytest
```

The tests use recording fake sinks and synthetic identifiers to prove that clinical raw text is absent from every provider submission.

## Durable handoff (v0.2)

`DurableProviderSink` adds an atomic local metadata journal around provider submission. It persists the handoff state before the network call, requires a caller-supplied stable idempotency key, and reuses that key after restart. The journal stores hashes and state only — never transcript text, egress text, or the plaintext idempotency key.

See `docs/durable-handoff.md`.

## Scope

The core remains provider-neutral and intentionally excludes production speech recognition, local-model runtimes, messaging-platform integrations, agent-framework internals, private databases, deployment configuration, and real patient data.

The included verifier is a demonstration safety primitive, **not** a complete de-identification standard, regulatory compliance claim, or medical device.

See `docs/architecture.md`, `docs/privacy-boundary.md`, `docs/threat-model.md`, `PROVENANCE.md`, and `CHANGELOG.md`.

## Release status

The current package version is `0.2.0`. Release gates are tracked in `docs/release-checklist.md`.

## Support the project

If you find this project useful and would like to support its continued development, donations are welcome.

**Ethereum / EVM:** `0xaace58c7fed05dc1095f5d88ca7b6f4c98986104`

Donations are completely optional and do not provide additional license rights, support guarantees, influence, or priority.

## License

Licensed under the Apache License, Version 2.0 (`Apache-2.0`). See `LICENSE`.
