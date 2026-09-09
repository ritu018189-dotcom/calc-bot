import json
import logging
import os
import threading
import time
from datetime import datetime
from types import SimpleNamespace

import telebot
from dotenv import load_dotenv
from flask import Flask

import handlers
from engines import CURRENCY_DB, MathEngine, YahooFinanceEngine, get_currency
from mfs_parser import TransactionStore

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is not set. "
        "Set it before starting the bot, e.g.: export BOT_TOKEN='your-token-here'"
    )

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("calc_bot")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

app = Flask(__name__)


@app.route("/")
def index():
    status = {
        "status": "online",
        "server_time": str(datetime.now()),
        "service": "Telegram Bot API",
        "load": "Normal",
    }
    return json.dumps(status, indent=4)


def run_server():
    app.run(host="0.0.0.0", port=8080)


def start_keep_alive():
    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()


deps = SimpleNamespace(
    finance_engine=YahooFinanceEngine(),
    math_engine=MathEngine(),
    transaction_store=TransactionStore(),
    get_currency=get_currency,
    currency_db=CURRENCY_DB,
    logger=logger,
)

handlers.register_all(bot, deps)


def start_bot():
    """Runs the bot with auto-restart capability"""
    while True:
        try:
            logger.info("Bot is connecting to Telegram Servers...")
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            logger.error(f"Connection Lost: {e}")
            time.sleep(5)
            logger.info("Reconnecting...")


if __name__ == "__main__":
    start_keep_alive()
    start_bot()
