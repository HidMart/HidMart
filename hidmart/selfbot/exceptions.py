class SelfBotError(Exception):
    """Base exception for HidMart SelfBot."""


class SelfBotConnectionError(SelfBotError):
    """Connection failed."""


class SelfBotAuthenticationError(SelfBotError):
    """Authentication failed."""


class SelfBotNotConnectedError(SelfBotError):
    """Client is not connected."""