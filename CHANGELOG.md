# Changelog

## Unreleased

### Added
- `/verify` command: parses bKash/Nagad/Rocket payment confirmation
  messages and blocks reuse of an already-verified TrxID
  (`mfs_parser/`).
- Package layout: `engines/` (finance, math, currency data),
  `handlers/` (one module per command), `mfs_parser/` (one module per
  provider).
- Per-currency data files under `data/currencies/`, replacing a single
  hardcoded dict; added several precious metals and cryptocurrencies not
  previously covered.
- Test suite (`tests/unit`, `tests/integration`) covering the math
  engine, each MFS parser, replay protection, currency data, the finance
  engine (mocked), and handler registration.
- CI (GitHub Actions): tests across Python 3.10–3.12, formatting checks,
  a Docker build check, and CodeQL scanning.
- Docker, Render, Railway, and systemd deployment configs under `deploy/`.
- Documentation under `docs/` (architecture, security model, per-command
  reference, per-MFS-provider format notes, deployment, FAQ).

### Changed
- `/calc` no longer uses `eval()` — expressions are parsed into an AST and
  evaluated against a fixed whitelist of operators/functions/constants.
- `BOT_TOKEN` is read from the environment (`.env` locally) instead of
  being hardcoded in source.
- `/time <city>` now actually looks up the timezone for the given city via
  `pytz`, instead of always printing server time.

### Security
- Removed a bot token that had been committed to source — if you're
  reusing this repo's history, treat that token as compromised and
  regenerate it via @BotFather.
