class NewMessage:

    def __init__(self, pattern=None):
        self.pattern = pattern

    def matches(self, message):

        if self.pattern is None:
            return True

        text = message.text or ""

        if callable(self.pattern):
            return bool(
                self.pattern(text)
            )

        return text.startswith(
            self.pattern
        )