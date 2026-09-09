def register(bot, deps):
    @bot.message_handler(commands=["calc"])
    def calculate(message):
        try:
            expression = message.text.replace("/calc", "").strip()
            if not expression:
                bot.reply_to(message, "⚠️ Write some math! Example: `/calc 10+20`")
                return

            result = deps.math_engine.solve(expression)
            bot.reply_to(message, f"🔢 **Result:** `{result}`")

        except Exception:
            bot.reply_to(message, "❌ Calculation Failed.")
