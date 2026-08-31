from hidmart import Bot


TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(TOKEN)


@bot.on_command("start")
async def start(message):
    await message.reply(
        "سلام 👋\n"
        "ربات HidMart با موفقیت اجرا شد."
    )


@bot.on_text("سلام")
async def hello(message):
    await message.reply(
        "سلام! ربات فعاله ✅"
    )


@bot.on_message()
async def messages(message):
    print(
        f"Message: {message.text}"
    )


bot.run()