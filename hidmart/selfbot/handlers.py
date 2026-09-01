import inspect


class HandlerManager:
    def __init__(self):
        self._message_handlers = []

    def add_message_handler(self, callback):
        self._message_handlers.append(callback)
        return callback

    async def dispatch_message(self, message):
        for callback in self._message_handlers:
            result = callback(message)

            if inspect.isawaitable(result):
                await result