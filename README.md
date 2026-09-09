# calc-bot

A Telegram bot for currency conversion, a scientific calculator, live
stock/crypto prices, world clock lookups, and MFS (bKash/Nagad/Rocket)
payment message verification — with an inline mode for use in any chat.

[![CI](https://github.com/ritu018189-dotcom/calc-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/ritu018189-dotcom/calc-bot/actions/workflows/ci.yml)
[![Lint](https://github.com/ritu018189-dotcom/calc-bot/actions/workflows/lint.yml/badge.svg)](https://github.com/ritu018189-dotcom/calc-bot/actions/workflows/lint.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- **Currency conversion** — `/convert 100 USD BDT`, live Yahoo Finance rates,
  177 currencies/cryptos/metals in `data/currencies/`
- **Scientific calculator** — `/calc sin(90) + sqrt(144)`, evaluated by a
  hand-rolled AST walker (no `eval()` — see [docs/security.md](docs/security.md))
- **Stock & crypto prices** — `/price BTC-USD`, `/price AAPL`
- **World clock** — `/time London`
- **MFS payment verification** — `/verify <pasted message>` parses
  bKash/Nagad/Rocket confirmation text and blocks reuse of an already-used
  TrxID (see [docs/security.md](docs/security.md) for what this does and
  doesn't prove)
- **Inline mode** — type `@your_bot 100 USD BDT` in any chat

See [docs/README.md](docs/README.md) for the full documentation index.

## Setup

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy its token.
2. Clone this repo and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Provide the bot token via an environment variable — never commit it to source:

   ```bash
   cp .env.example .env
   # edit .env and set BOT_TOKEN=<your token>
   ```

4. Run the bot:

   ```bash
   python main.py
   ```

The bot also starts a small Flask server on port `8080` for host platforms
(e.g. Render) that require an HTTP health check to keep the service alive.

## Deployment

Docker, Render, Railway, and systemd configs live under `deploy/` — see
[docs/guides/deployment.md](docs/guides/deployment.md).

```bash
docker build -t calc-bot .
docker run --env-file .env -p 8080:8080 calc-bot
```

## Tests

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

See [docs/guides/running_tests.md](docs/guides/running_tests.md).

## Project layout

```
main.py            bootstraps config, the bot, and the Flask health server
engines/            math evaluator, Yahoo Finance wrapper, currency data loader
handlers/           one module per bot command
mfs_parser/         bKash/Nagad/Rocket message parsers + replay guard
data/currencies/    one JSON file per currency/crypto/metal
docs/               architecture, security model, command & format reference
examples/           webhook alternative entrypoint, sample MFS messages
deploy/             Docker Compose, Render, Railway, systemd configs
scripts/            currency-data generator/validator, lint/test/format scripts
tests/              unit + integration test suite
```

Full breakdown in [docs/architecture.md](docs/architecture.md).

## Security note

If you ever commit a real bot token to a public repo, treat it as
compromised — revoke it via @BotFather (`/revoke` or `/token`) and issue a
new one. See [docs/security.md](docs/security.md) for the calculator
sandbox and MFS verification trust model.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
