from handler_test_utils import FakeBot, make_deps, make_message

from handlers.calc import register


class _StubMathEngine:
    def solve(self, expression):
        return "42" if expression.strip() == "40+2" else "❌ Syntax Error"


def _setup():
    bot = FakeBot()
    deps = make_deps(math_engine=_StubMathEngine())
    register(bot, deps)
    return bot


def test_calc_returns_result_for_valid_expression():
    bot = _setup()
    bot.call("calc", make_message("/calc 40+2"))
    assert bot.replies[-1] == "🔢 **Result:** `42`"


def test_calc_prompts_when_no_expression_given():
    bot = _setup()
    bot.call("calc", make_message("/calc"))
    assert "Write some math" in bot.replies[-1]
