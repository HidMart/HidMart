class Handler:

    def __init__(
        self,
        callback,
        command=None,
        text=None
    ):
        self.callback = callback
        self.command = command
        self.text = text


class HandlerManager:

    def __init__(self):
        self.handlers = []

    def add(
        self,
        callback,
        command=None,
        text=None
    ):
        handler = Handler(
            callback,
            command=command,
            text=text
        )

        self.handlers.append(handler)

        return callback

    async def dispatch(self, message):

        for handler in self.handlers:

            if handler.command is not None:

                text = message.text or ""

                if not text.startswith("/"):
                    continue

                command = text[1:].split()[0]

                if command != handler.command:
                    continue

            if handler.text is not None:

                if message.text != handler.text:
                    continue

            await handler.callback(message)