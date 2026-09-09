# Writing a handler

Every command lives in its own module under `handlers/`, exposing a single
`register(bot, deps)` function:

```python
# handlers/example.py
def register(bot, deps):
    @bot.message_handler(commands=["example"])
    def example_command(message):
        bot.reply_to(message, "Hello from /example")
```

Then register it in `handlers/__init__.py`:

```python
from . import calc, convert, example, help, inline, price, start, time_handler, verify

_MODULES = [start, help, convert, calc, price, time_handler, verify, example, inline]
```

## Using shared engines

`deps` is a plain `SimpleNamespace` (built in `main.py`) carrying
`finance_engine`, `math_engine`, `transaction_store`, `get_currency`, and
`logger`. Pull what you need off it rather than importing module-level
globals — that's what makes the handler testable without a real bot or
network access (see `tests/unit/test_handlers_calc.py` for the pattern:
build a fake `deps` with a stub engine, call the registered function
directly).

## Testing it

Use `tests/unit/handler_test_utils.py`'s `FakeBot`, `make_message`, and
`make_deps` to call your handler directly:

```python
from handler_test_utils import FakeBot, make_deps, make_message
from handlers.example import register

def test_example_replies_hello():
    bot = FakeBot()
    register(bot, make_deps())
    bot.call("example", make_message("/example"))
    assert bot.replies[-1] == "Hello from /example"
```
