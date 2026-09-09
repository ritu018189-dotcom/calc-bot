"""
Imports the real main.py entrypoint (with a dummy BOT_TOKEN) and checks that
every handler wired itself onto the bot, and that the keep-alive Flask app
responds — without ever calling Telegram's API or starting polling.
"""

import json


def test_all_commands_are_registered():
    import main

    registered_commands = set()
    for handler in main.bot.message_handlers:
        registered_commands.update(handler["filters"].get("commands") or [])

    for expected in {"start", "help", "convert", "calc", "price", "time", "verify"}:
        assert expected in registered_commands


def test_inline_handler_is_registered():
    import main

    assert len(main.bot.inline_handlers) >= 1


def test_flask_health_endpoint_reports_online():
    import main

    client = main.app.test_client()
    response = client.get("/")
    payload = json.loads(response.data)

    assert response.status_code == 200
    assert payload["status"] == "online"
