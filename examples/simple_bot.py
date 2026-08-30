import asyncio

from hidmart import Bot, Dispatcher


TOKEN = "YOUR_BALE_BOT_TOKEN"


async def main():
    bot = Bot(TOKEN)
    dispatcher = Dispatcher()

    @dispatcher.message
    async def on_message(message):
        print("Message:", message.text)

    await bot.start()

    print("HidMart bot started.")

    # Bot logic goes here.

    await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())