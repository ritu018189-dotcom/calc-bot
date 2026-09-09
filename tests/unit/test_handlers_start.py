from handler_test_utils import FakeBot, make_deps, make_message

from handlers.start import register


def test_start_greets_user_by_name():
    bot = FakeBot()
    register(bot, make_deps())
    bot.call("start", make_message("/start", first_name="Ritu"))
    assert "Hello Ritu" in bot.replies[-1]
    assert "/verify" in bot.replies[-1]
