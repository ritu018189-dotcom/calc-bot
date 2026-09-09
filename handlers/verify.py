from mfs_parser import parse_mfs_message


def register(bot, deps):
    @bot.message_handler(commands=["verify"])
    def verify_payment(message):
        try:
            text = message.text.replace("/verify", "", 1).strip()
            if not text:
                bot.reply_to(
                    message,
                    "⚠️ Paste the payment confirmation message after the command.\n"
                    "Example: `/verify You have received Tk 500.00 from "
                    "01712345678. Ref abc. Fee Tk 0.00. Balance Tk 5,000.00. "
                    "TrxID 8N7A6S5D4F at 10/10/2025 20:00`",
                )
                return

            txn = parse_mfs_message(text)
            if not txn:
                bot.reply_to(
                    message,
                    "❌ Couldn't recognize this as a bKash/Nagad/Rocket payment message.",
                )
                return

            if deps.transaction_store.is_used(txn.trx_id):
                bot.reply_to(
                    message,
                    f"⚠️ **Already used:** TrxID `{txn.trx_id}` was verified before. "
                    "This message can't be used again.",
                )
                return

            deps.transaction_store.mark_used(txn)
            bot.reply_to(
                message,
                (
                    f"✅ **Parsed {txn.provider} payment**\n"
                    f"Amount: Tk {txn.amount:,.2f}\n"
                    f"Sender: {txn.sender or 'N/A'}\n"
                    f"TrxID: `{txn.trx_id}`\n\n"
                    "Reminder: this confirms the message text is well-formed and "
                    "unused — it does not confirm the message actually came from "
                    "the provider. Only trust confirmation text forwarded from a "
                    "channel you control."
                ),
            )
        except Exception as e:
            deps.logger.error(f"Verify Error: {e}")
            bot.reply_to(message, "❌ Error verifying payment message.")
