"""
HidMart
=======

Async Python framework for building Bale Messenger bots.

Version: 0.4.0
"""

from .bot import Bot
from .types import Message, User, Chat
from .exceptions import (
    HidMartError,
    APIError,
    NetworkError,
    InvalidTokenError,
)

# SelfBot API
from .selfbot import (
    SelfBot,
    SelfBotMessage,
    SelfBotUser,
    SelfBotChat,
    Auth,
    AuthState,
    NewMessage,
    SelfBotError,
    SelfBotConnectionError,
    SelfBotAuthenticationError,
    SelfBotNotConnectedError,
)

__version__ = "0.4.0"
__author__ = "HidMart"
__license__ = "MIT"

__all__ = [
    # Main Bot
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

    # SelfBot Models
    "SelfBotMessage",
    "SelfBotUser",
    "SelfBotChat",

    # SelfBot Auth
    "Auth",
    "AuthState",

    # SelfBot Events
    "NewMessage",

    # SelfBot Exceptions
    "SelfBotError",
    "SelfBotConnectionError",
    "SelfBotAuthenticationError",
    "SelfBotNotConnectedError",
]