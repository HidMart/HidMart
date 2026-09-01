from hidmart.ui import (
    InlineButton,
    InlineKeyboard,
    KeyboardButton,
    ReplyKeyboard,
    RemoveKeyboard,
)


def test_inline_button_callback():
    button = InlineButton(
        "OK",
        callback_data="ok",
    )

    assert button.to_dict() == {
        "text": "OK",
        "callback_data": "ok",
    }


def test_inline_button_url():
    button = InlineButton(
        "GitHub",
        url="https://github.com/",
    )

    assert button.to_dict() == {
        "text": "GitHub",
        "url": "https://github.com/",
    }


def test_inline_keyboard():
    keyboard = InlineKeyboard()

    keyboard.row(
        InlineButton(
            "Yes",
            callback_data="yes",
        ),
        InlineButton(
            "No",
            callback_data="no",
        ),
    )

    assert keyboard.to_dict() == {
        "inline_keyboard": [
            [
                {
                    "text": "Yes",
                    "callback_data": "yes",
                },
                {
                    "text": "No",
                    "callback_data": "no",
                },
            ]
        ]
    }


def test_inline_keyboard_rows():
    keyboard = InlineKeyboard()

    keyboard.row(
        InlineButton(
            "One",
            callback_data="one",
        )
    )

    keyboard.row(
        InlineButton(
            "Two",
            callback_data="two",
        )
    )

    result = keyboard.to_dict()

    assert len(
        result["inline_keyboard"]
    ) == 2


def test_reply_keyboard():
    keyboard = ReplyKeyboard()

    keyboard.row(
        KeyboardButton("Start"),
        KeyboardButton("Help"),
    )

    assert keyboard.to_dict() == {
        "keyboard": [
            [
                {"text": "Start"},
                {"text": "Help"},
            ]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False,
    }


def test_remove_keyboard():
    keyboard = RemoveKeyboard()

    assert keyboard.to_dict() == {
        "remove_keyboard": True,
        "selective": False,
    }


def test_button_validation():
    try:
        InlineButton("")
    except ValueError:
        return

    raise AssertionError(
        "Empty button text must raise ValueError"
    )


def test_callback_url_exclusive():
    try:
        InlineButton(
            "Button",
            callback_data="test",
            url="https://example.com",
        )
    except ValueError:
        return

    raise AssertionError(
        "callback_data and url must be exclusive"
    )