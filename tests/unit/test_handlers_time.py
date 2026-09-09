from handler_test_utils import FakeBot, make_deps, make_message

from handlers.time_handler import register


def _setup():
    bot = FakeBot()
    register(bot, make_deps())
    return bot


def test_time_resolves_known_city():
    bot = _setup()
    bot.call("time", make_message("/time London"))
    assert "London" in bot.replies[-1]
    assert "Europe/London" in bot.replies[-1]


def test_time_prompts_when_no_city_given():
    bot = _setup()
    bot.call("time", make_message("/time"))
    assert "Example" in bot.replies[-1]


def test_time_reports_unknown_city():
    bot = _setup()
    bot.call("time", make_message("/time Nowhereville"))
    assert "Couldn't find a timezone" in bot.replies[-1]
