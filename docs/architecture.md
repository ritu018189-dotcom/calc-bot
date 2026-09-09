# Architecture

```
main.py            Bootstraps config, the bot instance, the Flask keep-alive
                    server, and wires handlers onto the bot. No business
                    logic lives here.

engines/            Stateless building blocks used by handlers.
  currency_db.py    Loads data/currencies/*.json into an in-memory dict.
  finance.py         Wraps yfinance for FX rates and stock/crypto prices.
  math_engine.py     AST-based safe expression evaluator (no eval()).

mfs_parser/          Parses bKash/Nagad/Rocket payment confirmation text
                      and guards against replaying the same TrxID twice.
  bkash.py, nagad.py, rocket.py   One parser module per provider.
  store.py            SQLite-backed used-TrxID tracker.

handlers/             One module per bot command (start, help, convert,
                      calc, price, time_handler, verify) plus inline.py for
                      inline-mode queries. Each module exposes
                      register(bot, deps), where `deps` is a plain
                      SimpleNamespace carrying the shared engines/logger so
                      handlers stay easy to unit test without a real bot.

data/currencies/      One JSON file per currency/crypto/metal code, used by
                      engines/currency_db.py. Add a new one to support a new
                      code — see docs/guides/adding_a_currency.md.

tests/
  unit/               Engine and parser logic, no network or Telegram calls.
  integration/        Imports the real main.py and checks handlers wired up
                      and the Flask health route responds.
  fixtures/           Sample MFS messages used by the parser tests.
```

## Why a dependency namespace instead of globals?

Handlers used to import module-level globals (`finance_engine`, `bot`,
`CURRENCY_DB`) directly, which made them impossible to unit test in
isolation. Passing a `deps` object into `register(bot, deps)` means a test
can construct a fake `deps` with mocked engines and call the registered
handler function directly, without touching Telegram or Yahoo Finance.
