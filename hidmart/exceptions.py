class HidMartError(Exception):
    """Base exception for HidMart."""


class APIError(HidMartError):
    """Raised when Bale API returns an error."""

    def __init__(self, description=None, error_code=None):
        self.description = description or "Unknown API error"
        self.error_code = error_code

        message = self.description

        if error_code is not None:
            message = f"[{error_code}] {message}"

        super().__init__(message)


class NetworkError(HidMartError):
    """Raised when a network request fails."""