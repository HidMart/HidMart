class InlineButton:
    def __init__(
        self,
        text,
        callback_data=None,
        url=None,
    ):
        self.text = text
        self.callback_data = callback_data
        self.url = url

    def to_dict(self):
        button = {
            "text": self.text,
        }

        if self.callback_data is not None:
            button["callback_data"] = self.callback_data

        if self.url is not None:
            button["url"] = self.url

        return button


class InlineKeyboard:
    def __init__(self):
        self.inline_keyboard = []

    def row(self, *buttons):
        self.inline_keyboard.append([
            button.to_dict()
            if isinstance(button, InlineButton)
            else {
                "text": str(button)
            }
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
        self.text = text

    def to_dict(self):
        return {
            "text": self.text
        }


class ReplyKeyboard:
    def __init__(
        self,
        resize_keyboard=True,
        one_time_keyboard=False,
    ):
        self.keyboard = []
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard

    def row(self, *buttons):
        self.keyboard.append([
            button.to_dict()
            if isinstance(button, KeyboardButton)
            else {
                "text": str(button)
            }
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
    def __init__(self):
        self.remove_keyboard = True

    def to_dict(self):
        return {
            "remove_keyboard": True
        }