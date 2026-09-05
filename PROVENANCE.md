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

A repository license must be selected only after the copyright holder confirms that they have the rights needed to license the public implementation and any protectable material influenced by the private reference.

Until a `LICENSE` file and corresponding package metadata are committed, do not assume permission to copy, redistribute, or modify this repository beyond rights provided by applicable law.

## Privacy boundary for contributions

Do not contribute real patient data, private transcripts, credentials, production configuration, private database contents, private filesystem paths, or deployment secrets. Tests and examples must use synthetic data only.
