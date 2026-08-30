from typing import Awaitable, Callable, List

from .types import Message


Handler = Callable[[Message], Awaitable[None]]


class Dispatcher:
    def __init__(self):
        self._handlers: List[Handler] = []

    def message(self, handler: Handler):
        self._handlers.append(handler)
        return handler

    async def dispatch(self, message: Message):
        for handler in self._handlers:
            await handler(message)