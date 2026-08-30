import hidmart


def test_import():
    assert hidmart.Bot is not None
    assert hidmart.Client is not None


def test_version():
    assert hidmart.__version__ == "1.0.0"