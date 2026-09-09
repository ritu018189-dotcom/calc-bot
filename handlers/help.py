def register(bot, deps):
    @bot.message_handler(commands=["help"])
    def help_message(message):
        text = (
            "🆘 **HELP & DOCUMENTATION**\n\n"
            "1️⃣ **Currency Conversion**\n"
            "Format: `/convert [Amount] [From] [To]`\n"
            "Example: `/convert 500 SAR BDT`\n"
            "Note: We use Yahoo Finance for 100% accurate market rates.\n\n"
            "2️⃣ **Calculator Usage**\n"
            "Format: `/calc [Expression]`\n"
            "Supported: +, -, *, /, ^, sin, cos, sqrt\n"
            "Example: `/calc sin(90) + 10^2`\n\n"
            "3️⃣ **Check Prices (Stocks/Crypto)**\n"
            "Format: `/price [Symbol]`\n"
            "Example: `/price BTC-USD` for Bitcoin\n"
            "Example: `/price GOOGL` for Google Stock\n\n"
            "4️⃣ **MFS Payment Verification**\n"
            "Format: `/verify [pasted message]`\n"
            "Parses a bKash/Nagad/Rocket confirmation message and rejects it if "
            "the same TrxID has already been used. This checks the message text "
            "only — always forward it from a channel you trust, never accept it "
            "typed directly from a customer."
        )
        bot.reply_to(message, text)
