# Release checklist

Use this checklist before publishing the first tagged release.

## Rights and provenance

- [x] Copyright holder explicitly authorized Apache-2.0 licensing for the public implementation.
- [x] `PROVENANCE.md` is reviewed and accurate as an engineering provenance record.
- [x] Apache License, Version 2.0 is explicitly selected by the copyright holder.
- [x] `LICENSE` contains the canonical Apache-2.0 text.
- [x] Package metadata declares the SPDX expression `Apache-2.0` and includes `LICENSE`.

## Privacy and security

- [x] Repository review found no credentials, private paths, production state, private database contents, or real transcripts.
- [x] Tests and examples contain synthetic data only.
- [x] NORMAL/CLINICAL privacy-boundary tests pass.
- [x] Fail-closed transform/verifier tests pass.
- [x] Durable handoff restart/idempotency tests pass.
- [x] Mutation checks demonstrate that privacy and no-resubmit regressions are detected.

## Build and CI

- [x] Clean editable install succeeds after the release metadata changes.
- [x] Full test suite passes on Python 3.11, 3.12, and 3.13 in GitHub Actions after the release metadata changes.
- [x] Version in `pyproject.toml` matches the intended `v0.2.0` tag.
- [x] `CHANGELOG.md` matches the release contents.

## Publish

- [ ] Create the `v0.2.0` tag only after the previous gates pass.
- [ ] Publish release notes from the changelog.
- [ ] Re-check the release artifact/tree rather than relying only on the working branch.
- [ ] Package-index publication, if desired later, is a separate explicit step.
