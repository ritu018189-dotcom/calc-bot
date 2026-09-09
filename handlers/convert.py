from datetime import datetime


def register(bot, deps):
    @bot.message_handler(commands=["convert"])
    def convert_currency(message):
        try:
            parts = message.text.split()
            if len(parts) != 4:
                bot.reply_to(
                    message, "⚠️ **Format Error:**\nUse: `/convert 100 USD BDT`"
                )
                return

            amount = float(parts[1])
            base = parts[2].upper()
            target = parts[3].upper()

            bot.send_chat_action(message.chat.id, "typing")

            rate = deps.finance_engine.get_currency_rate(base, target)

            if rate:
                result = amount * rate

                base_data = deps.get_currency(base)
                target_data = deps.get_currency(target)

                response = (
                    f"💱 **Exchange Rate (Live)**\n"
                    f"{base_data['flag']} **{amount} {base}**\n"
                    f"Checking Market Data... 📡\n"
                    f"⬇️\n"
                    f"{target_data['flag']} **{result:,.2f} {target}**\n"
                    f"📈 **Rate:** 1 {base} = {rate:.4f} {target}\n"
                    f"🕒 **Time:** {datetime.now().strftime('%I:%M %p')}"
                )
                bot.reply_to(message, response)
            else:
                bot.reply_to(
                    message, "❌ **Error:** Invalid Currency Code or API Down."
                )

        except ValueError:
            bot.reply_to(message, "❌ **Error:** Amount must be a number.")
        except Exception as e:
            deps.logger.error(f"Convert Error: {e}")
            bot.reply_to(message, "❌ System Error. Try again later.")
