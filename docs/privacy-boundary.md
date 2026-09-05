# Privacy boundary

The central invariant is asymmetric:

- `NORMAL`: a `RawTranscript` is explicitly eligible for external egress.
- `CLINICAL`: a `RawTranscript` is never eligible for external egress. Only verifier-minted `VerifiedSafeText` may cross the boundary.

The API uses separate `authorize_normal()` and `authorize_clinical()` methods so a clinical path has no normal code path that accepts raw text.

Failures before authorization are fail-closed: transform failure, verifier failure, verifier rejection, or unknown routing must produce zero provider calls.

This project demonstrates a software privacy boundary. It does not claim that the included example verifier is sufficient for regulatory compliance or complete de-identification.
