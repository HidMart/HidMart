import hidmart


TOKEN = "توکن_ربات_بله"

bot = hidmart.Bot(
    token=TOKEN,
    base_url="API_BASE_URL"
)


@bot.on_message()
def message_handler(data):
    chat = data.get("chat", {})
    chat_id = chat.get("id")

    text = data.get("text", "")

    if text == "/start":
        bot.send_message(
            chat_id,
            "سلام!\nبه ربات HidMart خوش آمدید."
        )

    elif text == "/help":
        bot.send_message(
            chat_id,
            "دستورات ربات:\n"
            "/start\n"
            "/help"
        )


bot.run()