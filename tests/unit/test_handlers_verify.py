from handler_test_utils import FakeBot, make_deps, make_message

from handlers.verify import register
from mfs_parser.store import TransactionStore

BKASH_MSG = (
    "You have received Tk 500.00 from 01712345678. Ref abc. "
    "Fee Tk 0.00. Balance Tk 5,000.00. TrxID 8N7A6S5D4F at 10/10/2025 20:00"
)


def _setup(tmp_path):
    bot = FakeBot()
    store = TransactionStore(str(tmp_path / "handler_test.db"))
    deps = make_deps(transaction_store=store)
    register(bot, deps)
    return bot, store


def test_verify_accepts_a_fresh_transaction(tmp_path):
    bot, store = _setup(tmp_path)
    bot.call("verify", make_message(f"/verify {BKASH_MSG}"))
    assert "Parsed bKash payment" in bot.replies[-1]
    store.close()


def test_verify_rejects_a_replayed_transaction(tmp_path):
    bot, store = _setup(tmp_path)
    bot.call("verify", make_message(f"/verify {BKASH_MSG}"))
    bot.call("verify", make_message(f"/verify {BKASH_MSG}"))
    assert "Already used" in bot.replies[-1]
    store.close()


def test_verify_rejects_unrecognized_text(tmp_path):
    bot, store = _setup(tmp_path)
    bot.call("verify", make_message("/verify not a payment message"))
    assert "Couldn't recognize" in bot.replies[-1]
    store.close()


def test_verify_prompts_when_empty(tmp_path):
    bot, store = _setup(tmp_path)
    bot.call("verify", make_message("/verify"))
    assert "Paste the payment confirmation" in bot.replies[-1]
    store.close()
