from abc import ABC, abstractmethod

from .exceptions import (
    SelfBotConnectionError,
    SelfBotNotImplementedError
)


class BaseTransport(ABC):

    @abstractmethod
    async def connect(self):
        raise NotImplementedError

    @abstractmethod
    async def close(self):
        raise NotImplementedError

    @abstractmethod
    async def request(
        self,
        method,
        **params
    ):
        raise NotImplementedError

    @abstractmethod
    async def updates(self):
        raise NotImplementedError


class WebTransport(BaseTransport):

    def __init__(
        self,
        session,
        endpoint=None,
        timeout=30
    ):
        self.session = session
        self.endpoint = endpoint
        self.timeout = timeout
        self.connected = False

    async def connect(self):

        if not self.session:
            raise SelfBotConnectionError(
                "A valid session is required."
            )

        # Web transport implementation
        # will be connected here.

        self.connected = True

    async def close(self):

        self.connected = False

    async def request(
        self,
        method,
        **params
    ):

        if not self.connected:
            raise SelfBotConnectionError(
                "SelfBot is not connected."
            )

        raise SelfBotNotImplementedError(
            "Web transport request is not configured."
        )

    async def updates(self):

        if not self.connected:
            raise SelfBotConnectionError(
                "SelfBot is not connected."
            )

        raise SelfBotNotImplementedError(
            "Web update stream is not configured."
        )