# Running tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

- `tests/unit/` — pure logic, no network calls, no real Telegram bot.
- `tests/integration/test_bot_smoke.py` — imports the real `main.py` (with a
  dummy `BOT_TOKEN` set by `tests/conftest.py`) and checks every command
  handler registered and the Flask health route responds. It never calls
  Telegram's API or starts polling.
- `tests/fixtures/` — sample MFS confirmation messages used by the parser
  tests; add new ones here when you encounter a real-world message format
  the parsers don't handle yet.
