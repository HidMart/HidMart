from hidmart import (
    Bot,
    Message,
    User,
    Chat,
    APIError,
    NetworkError,
)


def test_bot_creation():

    bot = Bot(
        "TEST_TOKEN"
    )

    assert bot.token == "TEST_TOKEN"

    assert bot.handlers == []

    assert bot.offset is None


def test_user():

    user = User(
        id=123,
        first_name="Ali",
        last_name="Test",
        username="ali",
    )

    assert user.id == 123

    assert user.username == "ali"

    assert user.full_name == "Ali Test"


def test_chat():

    chat = Chat(
        id=123,
        type="private",
    )

    assert chat.id == 123

    assert chat.is_private is True

    assert chat.is_group is False


def test_message():

    chat = Chat(
        id=123,
        type="private",
    )

    message = Message(
        message_id=1,
        chat=chat,
        text="Hello",
    )

    assert message.id == 1

    assert message.text == "Hello"