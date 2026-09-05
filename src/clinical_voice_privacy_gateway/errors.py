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


class HandoffError(PrivacyGatewayError):
    """Base class for durable provider handoff failures."""


class HandoffStateError(HandoffError):
    """Raised when durable state is invalid or conflicts with the current payload."""


class HandoffUncertainError(HandoffError):
    """Raised when remote admission may have happened but is not locally confirmed."""
