# Contributing

Contributions should preserve the core invariant: clinical RAW transcript text must never reach a provider sink.

Before opening a pull request:

1. Use synthetic data only.
2. Add or update a test for every privacy-boundary change.
3. Run `python -m pytest`.
4. Do not add provider credentials, production paths, private deployment state, or real clinical transcripts.
5. Keep provider integrations optional and outside the core privacy boundary.
