# Threat model

## Protected asset

Identifiable clinical transcript content before local de-identification and verification.

## Primary threat

A routing, transform, verifier, or integration bug accidentally sends clinical RAW text to an external provider.

## Security properties in v0.1

1. Route values are explicit and unknown values fail closed.
2. NORMAL and CLINICAL egress use separate boundary methods.
3. Clinical egress requires a verifier-minted `VerifiedSafeText` capability.
4. Transform errors, verifier errors, and verifier rejection happen before provider submission.
5. Tests record every provider payload and assert that synthetic clinical RAW never appears there.

## Additional v0.2 property

6. Durable handoff records are written before provider attempts; restart retries use the same explicit idempotency key, and accepted records do not resubmit. The journal never stores payload text.

## Out of scope for v0.2

- Complete medical de-identification or regulatory certification
- Speech-recognition security
- Model sandboxing
- Cross-process locking and distributed handoff coordination
- Real patient data
- Provider-specific authentication
