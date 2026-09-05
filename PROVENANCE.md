# Provenance

This repository contains a public, provider-neutral implementation of privacy-boundary ideas developed in a separate private system.

## Public implementation

The public package, tests, examples, and documentation in this repository were written specifically for this repository. Private repository history, deployment configuration, production state, model/runtime files, credentials, and real transcripts were not imported.

The public design was informed by an engineering review of a private reference implementation maintained by the project author. The reference was used to identify security invariants and failure modes such as route-dependent disclosure, fail-closed verification, idempotent handoff, and crash/restart recovery.

## Reference-code comparison

Before the current public v0.2 code state was prepared for licensing, a local textual comparison was run against the selected private reference snapshot used during the extraction review.

The comparison found no identical multi-line code block. A small number of isolated identical or structurally similar lines/tokens remained in ordinary Python idioms and in conceptually related areas such as regular-expression verification, validation checks, JSON parsing, and fsync-based durable writes.

This is an engineering provenance check, not a legal opinion or a guarantee of copyright independence.

## Third-party material

No model weights, speech-recognition implementations, local-model runtimes, messaging-platform adapters, private agent-framework code, or third-party source trees are vendored in this repository.

The package runtime currently uses only the Python standard library. Development and CI use external tools and GitHub Actions referenced through normal package/action dependencies; those projects retain their own licenses.

## Licensing status

On 2026-09-05, the copyright holder explicitly selected the Apache License, Version 2.0 for this public repository. The repository-level `LICENSE` file contains the Apache-2.0 license text and package metadata declares the SPDX expression `Apache-2.0`.

This license applies to the public repository content made available here. It does not grant rights to any separate private reference implementation, production deployment, model/runtime asset, credential, database, transcript, or third-party component that is not distributed as part of this repository.

## Privacy boundary for contributions

Do not contribute real patient data, private transcripts, credentials, production configuration, private database contents, private filesystem paths, or deployment secrets. Tests and examples must use synthetic data only.
