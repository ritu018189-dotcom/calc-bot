from telebot import types


def register(bot, deps):
    @bot.inline_handler(lambda query: len(query.query) > 0)
    def inline_manager(query):
        text = query.query.strip()
        results = []

        try:
            parts = text.split()

            # --- SCENARIO 1: Currency (e.g., 100 USD BDT) ---
            if len(parts) == 3 and parts[0].replace(".", "", 1).isdigit():
                amount = float(parts[0])
                base = parts[1].upper()
                target = parts[2].upper()

                rate = deps.finance_engine.get_currency_rate(base, target)

                if rate:
                    final_amount = amount * rate

                    base_flag = deps.get_currency(base).get("flag", "")
                    target_flag = deps.get_currency(target).get("flag", "")

                    title = (
                        f"{base_flag} {amount} {base} ➡️ "
                        f"{target_flag} {final_amount:.2f} {target}"
                    )
                    desc = f"Market Rate: 1 {base} = {rate:.4f} {target}"

                    results.append(
                        types.InlineQueryResultArticle(
                            id="1",
                            title=title,
                            description=desc,
                            input_message_content=types.InputTextMessageContent(
                                f"{title}\nRate: {rate:.4f}"
                            ),
                        )
                    )

            # --- SCENARIO 2: Calculator (e.g., 50+50) ---
            else:
                calc_res = deps.math_engine.solve(text)
                if "Error" not in calc_res:
                    results.append(
                        types.InlineQueryResultArticle(
                            id="2",
                            title=f"🔢 Calculate: {text}",
                            description=f"Result: {calc_res}",
                            input_message_content=types.InputTextMessageContent(
                                f"🔢 **{text}** = `{calc_res}`"
                            ),
                        )
                    )

            bot.answer_inline_query(query.id, results, cache_time=1)

        except Exception as e:
            deps.logger.error(f"Inline Error: {e}")
