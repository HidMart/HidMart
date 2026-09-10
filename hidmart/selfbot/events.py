import inspect
from collections import defaultdict


class EventDispatcher:

    def __init__(self):
        self._handlers = defaultdict(list)

    def add(self, event, handler):
        self._handlers[event].append(handler)
        return handler

    def remove(self, event, handler):
        if handler in self._handlers.get(event, []):
            self._handlers[event].remove(handler)

    async def emit(self, event, *args, **kwargs):
        for handler in tuple(self._handlers.get(event, [])):
            result = handler(*args, **kwargs)

            if inspect.isawaitable(result):
                await result

    def decorator(self, event):
        def wrapper(func):
            self.add(event, func)
            return func

        return wrapper