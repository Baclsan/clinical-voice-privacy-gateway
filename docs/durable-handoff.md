# Durable idempotent handoff

v0.2 adds an optional `DurableProviderSink` wrapper around any provider sink.

The local journal is written **before** each network attempt. The caller should use an opaque, non-sensitive stable idempotency key; the journal persists only its SHA-256 digest. It stores only:

- route and payload kind;
- payload SHA-256;
- SHA-256 of the stable idempotency key (not the key itself);
- attempt count;
- admission state;
- provider submission ID after confirmed acceptance.

It does **not** persist transcript or egress text.

## Crash window

A process can die after the provider accepted a request but before the local journal records `ACCEPTED`. On restart the journal may still say `IN_FLIGHT` or `ADMISSION_UNKNOWN`.

The only safe retry contract is:

1. rebuild the same boundary-authorized payload;
2. reuse the exact same idempotency key;
3. submit to a provider that deduplicates that key.

The tests simulate this crash window and prove that two transport attempts create one remote admission with an idempotent fake provider.

## Explicit key requirement

When `PrivacyGateway` is wired to `DurableProviderSink`, callers must supply an explicit stable `idempotency_key`. A fresh random key generated after restart cannot provide duplicate-admission protection.

## Current scope

v0.2 provides crash/restart durability for a single writer per idempotency key. Cross-process locking, distributed consensus, remote polling, and response delivery ledgers remain future work.
