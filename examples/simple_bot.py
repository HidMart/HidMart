from hidmart import Bot


bot = Bot(
    "YOUR_BOT_TOKEN"
)


@bot.on_command("start")
async def start(message):

    await message.reply(
        "سلام\n"
        "به ربات خوش آمدید"
    )


@bot.on_command("help")
async def help_command(message):

    await message.reply(
        "راهنمای ربات"
    )


@bot.on_message()
async def messages(message):

    await message.reply(
        f"شما گفتید:\n{message.text}"
    )


bot.run()