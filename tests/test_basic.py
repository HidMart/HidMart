from hidmart import (
    Bot,
    Message,
    User,
    Chat,
)


def test_version_import():
    import hidmart

    assert hasattr(
        hidmart,
        "__version__"
    )


def test_user():
    user = User(
        id=123,
        first_name="Ali",
        last_name="Test",
        username="ali",
    )

    assert user.id == 123
    assert user.full_name == "Ali Test"
    assert user.username == "ali"


def test_chat():
    chat = Chat(
        id=100,
        type="private",
    )

    assert chat.id == 100
    assert chat.is_private
    assert not chat.is_group


def test_message():
    chat = Chat(
        id=100,
        type="private",
    )

    user = User(
        id=123,
        first_name="Ali",
    )

    message = Message(
        message_id=1,
        chat=chat,
        from_user=user,
        text="سلام",
    )

    assert message.id == 1
    assert message.text == "سلام"
    assert message.sender.id == 123


def test_bot_creation():
    bot = Bot(
        "TEST_TOKEN"
    )

    assert bot.token == "TEST_TOKEN"
    assert bot.running is False