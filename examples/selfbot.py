from hidmart import SelfBot


client = SelfBot(
    "YOUR_OWN_SESSION"
)


@client.on_command("start")
async def start(message):

    await message.reply(
        "HidMart SelfBot 0.4.0"
    )


@client.on_text("سلام")
async def hello(message):

    await message.reply(
        "سلام 👋"
    )


@client.on_message()
async def messages(message):

    print(
        "Message:",
        message.text
    )


client.run()