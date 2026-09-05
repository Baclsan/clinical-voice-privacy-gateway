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

## Out of scope for v0.1

- Complete medical de-identification or regulatory certification
- Speech-recognition security
- Model sandboxing
- Durable crash recovery and idempotent network admission
- Real patient data
- Provider-specific authentication
