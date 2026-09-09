from handler_test_utils import FakeBot, make_deps, make_message

from handlers.help import register


def test_help_mentions_every_command():
    bot = FakeBot()
    register(bot, make_deps())
    bot.call("help", make_message("/help"))
    text = bot.replies[-1]
    for cmd in ["/convert", "/calc", "/price", "/verify"]:
        assert cmd in text
