def register(bot, deps):
    @bot.message_handler(commands=["price"])
    def check_price(message):
        try:
            symbol = message.text.replace("/price", "").strip().upper()
            if not symbol:
                bot.reply_to(message, "⚠️ Example: `/price BTC-USD`")
                return

            bot.send_chat_action(message.chat.id, "typing")
            price = deps.finance_engine.get_stock_price(symbol)

            if price:
                bot.reply_to(message, f"📈 **{symbol} Price:** ${price:,.2f}")
            else:
                bot.reply_to(message, f"❌ Symbol `{symbol}` not found.")
        except Exception:
            bot.reply_to(message, "❌ Error fetching price.")
