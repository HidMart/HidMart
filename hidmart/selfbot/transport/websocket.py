from __future__ import annotations

import asyncio

import websockets

from ..errors import ConnectionError


class BaleTransport:

    def __init__(
        self,
        url,
        token=None,
    ):

        self.url = url
        self.token = token
        self.websocket = None

    @property
    def connected(self):

        return (
            self.websocket is not None
            and not self.websocket.closed
        )

    def headers(self):

        headers = {
            "User-Agent":
                "HidMart-SelfBot/0.1.0",

            "Origin":
                "https://web.bale.ai",
        }

        if self.token:
            headers[
                "Authorization"
            ] = f"Bearer {self.token}"

        return headers

    async def connect(self):

        if self.connected:
            return

        try:

            self.websocket = (
                await websockets.connect(
                    self.url,
                    additional_headers=
                        self.headers(),
                    max_size=None,
                    ping_interval=20,
                )
            )

        except Exception as exc:

            self.websocket = None

            raise ConnectionError(
                str(exc)
            ) from exc

    async def send(
        self,
        payload,
    ):

        if not self.connected:
            await self.connect()

        try:

            await self.websocket.send(
                payload
            )

        except Exception as exc:

            await self.close()

            raise ConnectionError(
                str(exc)
            ) from exc

    async def receive(self):

        if not self.connected:
            await self.connect()

        try:

            data = (
                await self.websocket.recv()
            )

        except Exception as exc:

            await self.close()

            raise ConnectionError(
                str(exc)
            ) from exc

        if isinstance(
            data,
            str,
        ):
            return data.encode()

        return bytes(data)

    async def close(self):

        websocket = self.websocket

        self.websocket = None

        if websocket:

            try:
                await websocket.close()
            except Exception:
                pass