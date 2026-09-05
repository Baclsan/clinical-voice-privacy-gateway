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

See `docs/architecture.md`, `docs/privacy-boundary.md`, and `docs/threat-model.md`.

## License

License selection is pending provenance review. Do not assume that private reference implementations or third-party components are covered by this repository until explicitly documented.
