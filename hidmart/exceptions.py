class HidMartError(Exception):
    """Base exception for HidMart."""


class ConnectionError(HidMartError):
    """Raised when the connection to Bale fails."""


class AuthenticationError(HidMartError):
    """Raised when authentication fails."""


class APIError(HidMartError):
    """Raised when Bale returns an API error."""

    def __init__(self, message, code=None, response=None):
        super().__init__(message)
        self.code = code
        self.response = response


class TimeoutError(HidMartError):
    """Raised when an API request times out."""