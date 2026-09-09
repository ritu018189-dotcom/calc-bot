from handler_test_utils import FakeBot, make_deps, make_inline_query

from handlers.inline import register


class _StubFinanceEngine:
    def get_currency_rate(self, base, target):
        return 120.0


class _StubMathEngine:
    def solve(self, expression):
        return "100"


def _setup():
    bot = FakeBot()
    deps = make_deps(finance_engine=_StubFinanceEngine(), math_engine=_StubMathEngine())
    register(bot, deps)
    return bot


def test_inline_currency_query_returns_a_result():
    bot = _setup()
    bot.call_inline(make_inline_query("10 USD BDT"))
    assert len(bot.inline_answers) == 1
    assert "BDT" in bot.inline_answers[0].title


def test_inline_calculator_query_returns_a_result():
    bot = _setup()
    bot.call_inline(make_inline_query("50+50"))
    assert len(bot.inline_answers) == 1
    assert "Calculate" in bot.inline_answers[0].title
