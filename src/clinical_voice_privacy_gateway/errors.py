"""Public error types for fail-closed privacy processing."""


class PrivacyGatewayError(RuntimeError):
    """Base class for privacy-gateway failures."""


class RouteError(PrivacyGatewayError):
    """Raised when an input route is missing or unsupported."""


class TransformError(PrivacyGatewayError):
    """Raised when a local privacy transform cannot produce a candidate."""


class VerificationError(PrivacyGatewayError):
    """Raised when a candidate cannot be verified as safe for clinical egress."""


class BoundaryError(PrivacyGatewayError):
    """Raised when an object is not eligible for the requested egress path."""
