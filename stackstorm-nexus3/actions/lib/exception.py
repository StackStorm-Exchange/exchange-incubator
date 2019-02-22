
__all__ = [
    "InvalidParameterError",
    "MissingParameterError",
    "MissingProfileError",
    "ValidationFailError",
    "NexusClientNotInstantiatedError"
]


class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidParameterError(Error):
    """Raised when input parameter is not valid"""
    pass


class MissingParameterError(Error):
    """Raised when required parameter is missing"""
    pass


class MissingProfileError(Error):
    """Raised when connection profile is missing"""
    pass


class ValidationFailError(Error):
    """Raised when connection profile has missing required fields"""
    pass


class NexusClientNotInstantiatedError(Error):
    """Raised when nexus_client is not instantiated"""
    pass
