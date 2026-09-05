"""Clinical Voice Privacy Gateway public API."""

from .boundary import DisclosureBoundary
from .errors import BoundaryError, PrivacyGatewayError, RouteError, TransformError, VerificationError
from .pipeline import PrivacyGateway
from .provider import ProviderSink, Submission
from .routing import Route
from .transform import PrivacyTransform
from .types import CandidateSafeText, EgressPayload, RawTranscript, VerifiedSafeText
from .verifier import RegexPrivacyVerifier, VerificationDecision

__all__ = [
    "BoundaryError",
    "CandidateSafeText",
    "DisclosureBoundary",
    "EgressPayload",
    "PrivacyGateway",
    "PrivacyGatewayError",
    "PrivacyTransform",
    "ProviderSink",
    "RawTranscript",
    "RegexPrivacyVerifier",
    "Route",
    "RouteError",
    "Submission",
    "TransformError",
    "VerificationDecision",
    "VerificationError",
    "VerifiedSafeText",
]
