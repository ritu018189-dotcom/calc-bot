from handler_test_utils import FakeBot, make_deps, make_message

from handlers.convert import register


class _StubFinanceEngine:
    def __init__(self, rate):
        self.rate = rate

    def get_currency_rate(self, base, target):
        return self.rate


def _setup(rate):
    bot = FakeBot()
    deps = make_deps(finance_engine=_StubFinanceEngine(rate))
    register(bot, deps)
    return bot


def test_convert_reports_converted_amount():
    bot = _setup(rate=120.0)
    bot.call("convert", make_message("/convert 10 USD BDT"))
    reply = bot.replies[-1]
    assert "1,200.00 BDT" in reply
    assert "1 USD = 120.0000 BDT" in reply


def test_convert_rejects_wrong_argument_count():
    bot = _setup(rate=120.0)
    bot.call("convert", make_message("/convert 10 USD"))
    assert "Format Error" in bot.replies[-1]


def test_convert_rejects_non_numeric_amount():
    bot = _setup(rate=120.0)
    bot.call("convert", make_message("/convert ten USD BDT"))
    assert "Amount must be a number" in bot.replies[-1]


def test_convert_reports_error_when_no_rate_found():
    bot = _setup(rate=None)
    bot.call("convert", make_message("/convert 10 XXX YYY"))
    assert "Invalid Currency Code" in bot.replies[-1]
