from hidmart import Bot


def test_bot_creation():

    bot = Bot(
        "TEST_TOKEN"
    )

    assert bot.token == "TEST_TOKEN"
    assert bot.handlers == []