# Clinical Voice Privacy Gateway

Local-first privacy infrastructure for clinical voice AI workflows.

The project explores a simple security boundary: identifiable clinical audio and raw transcripts should be processed locally before any external AI provider receives text. Normal non-clinical voice traffic may follow a separate route.

## Core idea

```text
Voice input
    |
    v
Local speech-to-text
    |
    v
Route selection
    |
    +---------------- NORMAL ----------------> application / AI provider
    |
    +--------------- CLINICAL
                         |
                         v
                local de-identification
                         |
                         v
                deterministic verifier
                         |
                         v
                  VERIFIED SAFE
                         |
                         v
                application / AI provider
```

## Design goals

- Local-first handling of identifiable clinical content
- Routing before disclosure to external providers
- Fail-closed privacy decisions
- Deterministic verification of de-identified output
- Clear separation between raw and safe data
- Testable privacy invariants
- Provider-agnostic interfaces

## Non-goals

This repository is not a medical device and does not provide medical advice, diagnosis, or treatment. It is an experimental software project focused on privacy architecture for voice-enabled AI systems.

## Privacy rule

Real patient data, credentials, production configuration, private transcripts, and deployment-specific secrets must never be committed to this repository. Examples and tests should use synthetic data only.

## Status

Early open-source extraction and design phase. The initial public implementation will be derived as a clean-room-style, deployment-neutral package rather than publishing private production history or configuration.

## Planned structure

```text
src/                 reusable privacy gateway components
tests/               privacy and routing invariants
docs/                architecture and threat model
examples/synthetic/  synthetic demonstration inputs
.github/workflows/   CI
```

## Security

Security and privacy issues will be documented in `SECURITY.md` as the project matures. Please do not include real clinical or personally identifiable data in reports.

## License

License selection is pending a provenance review of any code that may be extracted into the public implementation.
