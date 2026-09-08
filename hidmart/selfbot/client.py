from __future__ import annotations

import asyncio
import os

from .errors import AuthenticationError
from .events import EventDispatcher
from .rpc import RPCClient
from .session import Session
from .transport import BaleTransport


DEFAULT_URL = os.getenv(
    "HIDMART_BALE_WS_URL",
    "wss://next-ws.bale.ai",
)


class SelfBot:

    def __init__(
        self,
        token=None,
        *,
        session="hidmart.session.json",
        url=DEFAULT_URL,
    ):

        self.session = Session(
            session
        )

        if token:
            self.session.set(
                token
            )
        else:
            self.session.load()

        self.transport = BaleTransport(
            url,
            self.session.access_token,
        )

        self.rpc = RPCClient(
            self.transport
        )

        self.events = (
            EventDispatcher()
        )

        self.running = False
        self._task = None

    @property
    def authorized(self):

        return self.session.authorized

    @property
    def connected(self):

        return self.transport.connected

    def set_token(
        self,
        token,
    ):

        self.session.set(
            token
        )

        self.session.save()

        self.transport.token = token

    def on(
        self,
        event,
    ):

        return self.events.decorator(
            event
        )

    def on_message(self):

        return self.on(
            "message"
        )

    def on_update(self):

        return self.on(
            "update"
        )

    async def connect(self):

        if not self.authorized:
            raise AuthenticationError(
                "SelfBot is not authorized"
            )

        await self.transport.connect()

        await self.events.emit(
            "connected",
            self,
        )

    async def _reader(self):

        while self.running:

            try:

                data = (
                    await self.transport.receive()
                )

                await self.events.emit(
                    "raw",
                    data,
                )

                await self.events.emit(
                    "update",
                    data,
                )

            except asyncio.CancelledError:
                raise

            except Exception as exc:

                await self.events.emit(
                    "error",
                    exc,
                )

                await asyncio.sleep(
                    2
                )

                try:
                    await self.transport.connect()
                except Exception:
                    pass

    async def start(self):

        await self.connect()

        if self.running:
            return

        self.running = True

        self._task = (
            asyncio.create_task(
                self._reader()
            )
        )

        await self.events.emit(
            "started",
            self,
        )

    async def run(self):

        await self.start()

        try:

            while self.running:
                await asyncio.sleep(
                    3600
                )

        finally:

            await self.stop()

    async def stop(self):

        self.running = False

        if self._task:

            self._task.cancel()

            try:
                await self._task
            except asyncio.CancelledError:
                pass

            self._task = None

        await self.transport.close()

        await self.events.emit(
            "stopped",
            self,
        )

    async def disconnect(self):

        await self.stop()