HidMart

<div align="center">HidMart

Async Python Framework for Bale Messenger Bots

""Python" (https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)" (https://www.python.org/)
""GitHub" (https://img.shields.io/badge/GitHub-HidMart-black?logo=github)" (https://github.com/programmersatlantis-hash/HidMart)
""License" (https://img.shields.io/badge/License-MIT-green.svg)" (https://github.com/programmersatlantis-hash/HidMart)

</div>---

Installation

Install the latest version of HidMart directly from GitHub.

Install with pip

pip install https://github.com/programmersatlantis-hash/HidMart/archive/main.zip --force-reinstall

Install from source

git clone https://github.com/programmersatlantis-hash/HidMart.git
cd HidMart
pip install .

---

Quick Start

Create your first Bale bot with HidMart:

import asyncio
import hidmart


async def main():

    bot = hidmart.Bot(
        token="YOUR_BOT_TOKEN"
    )

    @bot.on_message()
    async def handler(message):

        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text == "/start":
            await bot.send_message(
                chat_id,
                "سلام! به ربات HidMart خوش آمدید."
            )

        elif text == "/help":
            await bot.send_message(
                chat_id,
                "دستورات:\n"
                "/start\n"
                "/help"
            )

    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())

---

Features

- Async Python architecture
- Bale bot support
- Message handlers
- Callback handlers
- Sending messages
- Sending photos
- Sending documents
- Inline keyboards
- Message editing
- Message deletion
- Error handling
- Type hints
- Lightweight architecture
- Easy to use API

---

Message Handler

Receive messages using a simple decorator:

@bot.on_message()
async def handler(message):

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    print(text)

---

Send Message

Send messages to Bale chats:

await bot.send_message(
    chat_id,
    "Hello from HidMart!"
)

---

Callback Handler

Handle callback interactions:

@bot.on_callback()
async def callback_handler(callback):

    print(callback)

---

Error Handling

HidMart provides its own exception classes:

from hidmart.exceptions import (
    HidMartError,
    APIError,
    NetworkError,
    InvalidTokenError,
)

Example:

try:

    await bot.send_message(
        chat_id,
        "Hello!"
    )

except NetworkError:
    print("Network error")

except APIError as error:
    print(f"API error: {error}")

---

Type Support

HidMart includes typed objects for common Bale data:

from hidmart.types import (
    User,
    Chat,
    Message,
)

---

Requirements

- Python 3.9+
- Bale bot token
- Internet connection

---

Testing

Run the test suite with:

pytest

---

Contributing

Contributions are welcome.

If you find a bug, have an idea, or want to improve HidMart, feel free to open an issue or submit a pull request.

---

License

HidMart is released under the MIT License.

---

<div align="center">HidMart

Async Python Framework for Bale Messenger Bots

"GitHub" (https://github.com/programmersatlantis-hash/HidMart)

</div>