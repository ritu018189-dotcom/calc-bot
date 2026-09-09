from datetime import datetime

import pytz


def register(bot, deps):
    @bot.message_handler(commands=["time"])
    def world_time(message):
        try:
            location = message.text.replace("/time", "").strip()
            if not location:
                bot.reply_to(message, "⚠️ Example: `/time London`")
                return

            query = location.lower().replace(" ", "_")
            match = None
            for tz_name in pytz.all_timezones:
                city = tz_name.split("/")[-1].lower()
                if city == query or query in city:
                    match = tz_name
                    break

            if not match:
                bot.reply_to(message, f"❌ Couldn't find a timezone for `{location}`.")
                return

            now = datetime.now(pytz.timezone(match))
            bot.reply_to(
                message,
                f"🕒 **{location.title()}** ({match})\n{now.strftime('%Y-%m-%d %I:%M:%S %p')}",
            )
        except Exception as e:
            deps.logger.error(f"Time Error: {e}")
            bot.reply_to(message, "❌ Error fetching world time.")
