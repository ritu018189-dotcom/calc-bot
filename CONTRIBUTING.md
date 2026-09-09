# Contributing

1. Fork and clone the repo.
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt -r requirements-dev.txt`
4. Copy `.env.example` to `.env` and set your own `BOT_TOKEN` for local testing.
5. Make your change. See `docs/architecture.md` for how the pieces fit
   together before adding a new handler/engine.
6. Run `bash scripts/format.sh` then `bash scripts/lint.sh` and `pytest`.
7. Open a PR using the template — check the boxes that actually apply.

## Where things live

- New bot command → add a module under `handlers/`, register it in
  `handlers/__init__.py`.
- New currency → `docs/guides/adding_a_currency.md`.
- New MFS provider → `docs/guides/adding_an_mfs_provider.md`.

## Commit messages

Explain *why*, not just *what* — the diff already shows what changed.
