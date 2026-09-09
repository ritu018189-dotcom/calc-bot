from handler_test_utils import FakeBot, make_deps, make_message

from handlers.price import register


class _StubFinanceEngine:
    def __init__(self, price):
        self.price = price

    def get_stock_price(self, symbol):
        return self.price


def _setup(price):
    bot = FakeBot()
    deps = make_deps(finance_engine=_StubFinanceEngine(price))
    register(bot, deps)
    return bot


def test_price_reports_value():
    bot = _setup(price=65000.5)
    bot.call("price", make_message("/price BTC-USD"))
    assert "$65,000.50" in bot.replies[-1]


def test_price_prompts_when_no_symbol():
    bot = _setup(price=100.0)
    bot.call("price", make_message("/price"))
    assert "Example" in bot.replies[-1]


def test_price_reports_not_found():
    bot = _setup(price=None)
    bot.call("price", make_message("/price BOGUS"))
    assert "not found" in bot.replies[-1]
