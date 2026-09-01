from .bot import Bot
from .types import Message, User, Chat

from .exceptions import (
    HidMartError,
    APIError,
    NetworkError,
    InvalidTokenError,
)

# SelfBot
from .selfbot import (
    SelfBot,
    SelfBotMessage,
    SelfBotUser,
    SelfBotChat,
)

from .selfbot.exceptions import (
    SelfBotError,
    SelfBotConnectionError,
    SelfBotAuthenticationError,
    SelfBotAPIError,
    SelfBotNotImplementedError,
)


__version__ = "0.4.0"


__all__ = [
    # Bot
    "Bot",

    # Bot Types
    "Message",
    "User",
    "Chat",

    # Bot Exceptions
    "HidMartError",
    "APIError",
    "NetworkError",
    "InvalidTokenError",

    # SelfBot
    "SelfBot",
    "SelfBotMessage",
    "SelfBotUser",
    "SelfBotChat",

    # SelfBot Exceptions
    "SelfBotError",
    "SelfBotConnectionError",
    "SelfBotAuthenticationError",
    "SelfBotAPIError",
    "SelfBotNotImplementedError",
]