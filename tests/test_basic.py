import pytest

from hidmart import (
    APIError,
    AuthenticationError,
    BaleClient,
    Bot,
    Chat,
    Dispatcher,
    Message,
    User,
)


def test_imports():
    assert BaleClient is not None
    assert Bot is not None
    assert Dispatcher is not None


def test_user():
    user = User.from_dict({
        "id": 123,
        "first_name": "Ali",
        "username": "ali",
    })

    assert user.id == "123"
    assert user.first_name == "Ali"


def test_message():
    message = Message.from_dict({
        "id": 10,
        "text": "Hello",
        "chat_id": 20,
        "sender_id": 30,
    })

    assert message.id == "10"
    assert message.text == "Hello"
    assert message.chat_id == "20"


def test_chat():
    chat = Chat.from_dict({
        "id": 100,
        "title": "Test",
        "type": "group",
    })

    assert chat.id == "100"
    assert chat.title == "Test"


def test_empty_token():
    with pytest.raises(AuthenticationError):
        BaleClient("")


@pytest.mark.asyncio
async def test_connect():
    client = BaleClient("test-token")

    await client.connect()

    assert client.connected is True

    await client.close()

    assert client.connected is False