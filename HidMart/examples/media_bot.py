from hidmart import Bot


bot = Bot("TOKEN")


@bot.on_command("start")
async def start(message):

    await message.reply(
        "سلام 👋\n\n"
        "عکس، ویدیو، فایل، صوت یا Voice بفرست."
    )


@bot.on_photo()
async def photo(message):

    print("PHOTO:")
    print(message.photo)

    await message.reply(
        "عکس دریافت شد ✅"
    )


@bot.on_video()
async def video(message):

    print("VIDEO:")
    print(message.video)

    await message.reply(
        "ویدیو دریافت شد ✅"
    )


@bot.on_document()
async def document(message):

    print("DOCUMENT:")
    print(message.document)

    await message.reply(
        "فایل دریافت شد ✅"
    )


@bot.on_audio()
async def audio(message):

    await message.reply(
        "Audio دریافت شد ✅"
    )


@bot.on_voice()
async def voice(message):

    await message.reply(
        "Voice دریافت شد ✅"
    )


@bot.on_sticker()
async def sticker(message):

    await message.reply(
        "Sticker دریافت شد ✅"
    )


@bot.on_location()
async def location(message):

    print(message.location)

    await message.reply(
        "Location دریافت شد 📍"
    )


@bot.on_media()
async def any_media(message):

    print("RAW:")
    print(message.raw)


bot.run()