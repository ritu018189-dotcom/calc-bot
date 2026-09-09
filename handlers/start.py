from telebot import types


def register(bot, deps):
    @bot.message_handler(commands=["start"])
    def welcome_message(message):
        user = message.from_user.first_name
        text = (
            f"👋 **Hello {user}!**\n\n"
            "Welcome!\n"
            "I am powered by Google/Yahoo Finance Real-Time Data.\n\n"
            "🛠 **MY FEATURES:**\n"
            "💱 **Currency Converter**\n"
            "`/convert 100 USD BDT`\n\n"
            "🧮 **Scientific Calculator**\n"
            "`/calc 50 + sqrt(144)`\n\n"
            "📈 **Stock/Crypto Price**\n"
            "`/price BTC-USD` (Bitcoin)\n"
            "`/price AAPL` (Apple)\n\n"
            "🌍 **World Time**\n"
            "`/time London`\n\n"
            "🧾 **MFS Payment Verify**\n"
            "`/verify <paste bKash/Nagad/Rocket message>`\n\n"
            "🔍 **Inline Mode:** Type `@mybot 100 USD BDT` in any chat."
        )

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(
            "👨‍💻 Developer", url="https://t.me/YOUR_USER_NAME"
        )
        btn2 = types.InlineKeyboardButton("📜 Currency List", callback_data="show_list")
        markup.add(btn1, btn2)

        bot.reply_to(message, text, reply_markup=markup)
