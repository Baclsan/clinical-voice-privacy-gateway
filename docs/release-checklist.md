# Release checklist

Use this checklist before publishing the first tagged release.

## Rights and provenance

- [ ] Copyright holder confirms the right to license the public implementation.
- [ ] `PROVENANCE.md` is reviewed and accurate.
- [ ] A specific open-source license is explicitly selected by the copyright holder.
- [ ] `LICENSE` is added with the exact canonical license text.
- [ ] Package metadata is updated to the selected SPDX license identifier where appropriate.

## Privacy and security

- [ ] Repository scan finds no credentials, private paths, production state, private database contents, or real transcripts.
- [ ] Tests and examples contain synthetic data only.
- [ ] NORMAL/CLINICAL privacy-boundary tests pass.
- [ ] Fail-closed transform/verifier tests pass.
- [ ] Durable handoff restart/idempotency tests pass.
- [ ] Mutation checks still demonstrate that privacy and no-resubmit regressions are detected.

## Build and CI

- [ ] Clean editable install succeeds.
- [ ] Full test suite passes on all supported Python versions in GitHub Actions.
- [ ] Version in `pyproject.toml` matches the intended tag.
- [ ] `CHANGELOG.md` matches the release contents.

## Publish

- [ ] Create an annotated or GitHub release tag only after the previous gates pass.
- [ ] Publish release notes from the changelog.
- [ ] Re-check the release artifact/tree rather than relying only on the working branch.
- [ ] Package-index publication, if desired later, is a separate explicit step.
