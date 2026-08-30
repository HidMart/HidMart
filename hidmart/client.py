import asyncio
from typing import Any, Dict, Optional

from .exceptions import (
    APIError,
    AuthenticationError,
    ConnectionError,
)


class BaleClient:
    """
    Async client for HidMart.

    The transport layer is intentionally kept separate from
    the higher-level bot API.
    """

    def __init__(
        self,
        token: str,
        base_url: str = "https://tapi.bale.ai",
        timeout: float = 30.0,
    ):
        if not token:
            raise AuthenticationError("Bot token is required.")

        self.token = token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.session = None
        self.connected = False

    async def connect(self):
        """
        Initialize the client.

        The actual Bale transport can be plugged into this layer
        without changing the bot interface.
        """
        self.connected = True
        return self

    async def close(self):
        if self.session is not None:
            close = getattr(self.session, "close", None)

            if close is not None:
                result = close()

                if asyncio.iscoroutine(result):
                    await result

        self.session = None
        self.connected = False

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def request(
        self,
        method: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Low-level API request.

        This method is the central point for implementing
        the real Bale transport.
        """
        if not self.connected:
            raise ConnectionError(
                "Client is not connected. Call await client.connect()."
            )

        raise NotImplementedError(
            "Bale transport has not been configured yet."
        )

    async def call(
        self,
        service: str,
        method: str,
        **kwargs,
    ):
        """
        Call a service method.

        Example:

            await client.call(
                "Messaging",
                "SomeMethod",
                chat_id="123",
            )
        """

        return await self.request(
            f"{service}.{method}",
            kwargs,
        )