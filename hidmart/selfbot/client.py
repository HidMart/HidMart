import asyncio

from .auth import Auth
from .events import NewMessage
from .handlers import HandlerManager
from .transport import Transport
from .models import SelfBotMessage
from .exceptions import SelfBotNotConnectedError


class SelfBot:
    def __init__(self, transport=None):
        self.transport = transport or Transport()
        self.auth = Auth()
        self.handlers = HandlerManager()
        self._running = False

    async def connect(self):
        await self.transport.connect()
        return self

    async def disconnect(self):
        self._running = False
        await self.transport.disconnect()

    @property
    def is_connected(self):
        return self.transport.connected

    def on_message(self):
        def decorator(callback):
            self.handlers.add_message_handler(callback)
            return callback

        return decorator

    async def dispatch(self, message):
        event = NewMessage(message)
        await self.handlers.dispatch_message(event)

    async def get_me(self):
        if not self.is_connected:
            raise SelfBotNotConnectedError()

        return self.auth.state

    async def run_until_disconnected(self):
        if not self.is_connected:
            raise SelfBotNotConnectedError()

        self._running = True

        try:
            while self._running:
                await asyncio.sleep(1)
        finally:
            self._running = False