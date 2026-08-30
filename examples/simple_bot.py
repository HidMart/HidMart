from hidmart import Bot


bot = Bot(
    "YOUR_BOT_TOKEN"
)


@bot.on_command("start")
async def start(message):

    await message.reply(
        "سلام 👋\n"
        "ربات با HidMart اجرا شد!"
    )


@bot.on_command(
    "help",
    "راهنما"
)
async def help_command(message):

    await message.reply(
        "راهنمای ربات\n\n"
        "/start - شروع\n"
        "/help - راهنما"
    )


@bot.on_text("سلام")
async def hello(message):

    await message.reply(
        "سلام! 👋"
    )


@bot.on_message()
async def messages(message):

    if not message.text:
        return

    await message.reply(
        f"شما گفتید:\n{message.text}"
    )


bot.run()