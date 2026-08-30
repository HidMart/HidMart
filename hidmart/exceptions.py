class HidMartError(Exception):
    """Base exception for HidMart."""
    pass


class APIError(HidMartError):
    """Raised when Bale API returns an error."""
    pass


class NetworkError(HidMartError):
    """Raised when a network request fails."""
    pass


class InvalidTokenError(HidMartError):
    """Raised when the bot token is invalid."""
    pass