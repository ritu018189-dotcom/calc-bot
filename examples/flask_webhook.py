"""
Alternative entrypoint: receive Telegram updates via webhook instead of the
long-polling loop in main.py's start_bot(). Not used by default — main.py's
polling approach needs no public URL and is simpler to run locally, but a
webhook avoids an always-open long-poll connection and can suit some hosts
better.

Usage:
    export BOT_TOKEN=...
    export WEBHOOK_URL=https://your-host.example.com/webhook
    python examples/flask_webhook.py
"""

# isort:skip_file
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import telebot  # noqa: E402
from flask import Flask, request  # noqa: E402

from main import bot  # noqa: E402  (reuses the already-configured, handler-wired bot)

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise RuntimeError(
        "Set WEBHOOK_URL to your public HTTPS endpoint, e.g. https://host/webhook"
    )

webhook_app = Flask(__name__)


@webhook_app.route("/webhook", methods=["POST"])
def receive_update():
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    webhook_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
