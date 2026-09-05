from clinical_voice_privacy_gateway import CandidateSafeText, RawTranscript, RegexPrivacyVerifier


def test_residual_synthetic_phone_is_rejected():
    raw = RawTranscript.from_text("Пациент Иванов Алексей Олегович, телефон +7 999 123-45-67.")
    candidate = CandidateSafeText("Пациент [PERSON], телефон +7 999 123-45-67.")

    decision = RegexPrivacyVerifier().verify(raw, candidate)

    assert not decision.passed
    assert "RESIDUAL_PHONE" in decision.reasons
    assert decision.safe is None


def test_residual_synthetic_dob_is_rejected():
    raw = RawTranscript.from_text("Пациент Иванов Алексей Олегович, дата рождения 12.03.1985, кашель.")
    candidate = CandidateSafeText("Пациент [PERSON], дата рождения 12.03.1985, кашель.")

    decision = RegexPrivacyVerifier().verify(raw, candidate)

    assert not decision.passed
    assert "RESIDUAL_DOB" in decision.reasons


def test_deidentified_candidate_mints_verified_safe_text():
    raw = RawTranscript.from_text("Пациент Иванов Алексей Олегович, телефон +7 999 123-45-67, кашель.")
    candidate = CandidateSafeText("Пациент [PERSON], телефон [PHONE], кашель.")

    decision = RegexPrivacyVerifier().verify(raw, candidate)

    assert decision.passed
    assert decision.reasons == ()
    assert decision.safe is not None
    assert decision.safe.text == candidate.text
