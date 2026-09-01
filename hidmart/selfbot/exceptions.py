class SelfBotError(Exception):
    """Base exception for HidMart SelfBot."""


class SelfBotConnectionError(SelfBotError):
    """Connection error."""


class SelfBotAuthenticationError(SelfBotError):
    """Authentication error."""


class SelfBotAPIError(SelfBotError):
    """API error."""


class SelfBotNotImplementedError(SelfBotError):
    """Transport operation is not implemented."""