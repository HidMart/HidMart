class InlineButton:
    def __init__(self, text, callback_data=None, url=None):
        if not text:
            raise ValueError("button text is required")

        if callback_data is not None and url is not None:
            raise ValueError(
                "callback_data and url cannot be used together"
            )

        self.text = text
        self.callback_data = callback_data
        self.url = url

    def to_dict(self):
        data = {
            "text": self.text,
        }

        if self.callback_data is not None:
            data["callback_data"] = self.callback_data

        if self.url is not None:
            data["url"] = self.url

        return data


class InlineKeyboard:
    def __init__(self, rows=None):
        self.inline_keyboard = []

        if rows:
            for row in rows:
                self.row(*row)

    def row(self, *buttons):
        if not buttons:
            raise ValueError("keyboard row cannot be empty")

        self.inline_keyboard.append([
            button.to_dict()
            if isinstance(button, InlineButton)
            else InlineButton(str(button)).to_dict()
            for button in buttons
        ])

        return self

    def add_button(
        self,
        text,
        callback_data=None,
        url=None,
    ):
        return self.row(
            InlineButton(
                text,
                callback_data=callback_data,
                url=url,
            )
        )

    def to_dict(self):
        return {
            "inline_keyboard": self.inline_keyboard
        }


class KeyboardButton:
    def __init__(self, text):
        if not text:
            raise ValueError("button text is required")

        self.text = text

    def to_dict(self):
        return {
            "text": self.text
        }


class ReplyKeyboard:
    def __init__(
        self,
        rows=None,
        resize_keyboard=True,
        one_time_keyboard=False,
    ):
        self.keyboard = []
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard

        if rows:
            for row in rows:
                self.row(*row)

    def row(self, *buttons):
        if not buttons:
            raise ValueError("keyboard row cannot be empty")

        self.keyboard.append([
            button.to_dict()
            if isinstance(button, KeyboardButton)
            else KeyboardButton(str(button)).to_dict()
            for button in buttons
        ])

        return self

    def add_button(self, text):
        return self.row(
            KeyboardButton(text)
        )

    def to_dict(self):
        return {
            "keyboard": self.keyboard,
            "resize_keyboard": self.resize_keyboard,
            "one_time_keyboard": self.one_time_keyboard,
        }


class RemoveKeyboard:
    def __init__(self, selective=False):
        self.selective = selective

    def to_dict(self):
        return {
            "remove_keyboard": True,
            "selective": self.selective,
        }