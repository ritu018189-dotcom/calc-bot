# FAQ

**Does `/verify` guarantee a payment is real?**
No — see [docs/security.md](security.md). It parses message text and blocks
reuse of the same TrxID; it does not call bKash/Nagad/Rocket's servers.

**Why not use `eval()` for the calculator?**
`eval()` with a character blocklist is a well-known way to end up with a
sandbox escape once someone finds a combination of allowed characters that
reaches Python internals. `engines/math_engine.py` walks a parsed AST
instead, so only whitelisted operations are ever reachable — see
[docs/security.md](security.md).

**How do I add a currency the bot doesn't know about?**
See [docs/guides/adding_a_currency.md](guides/adding_a_currency.md) — it's
one JSON file, no code changes.

**How do I add another MFS provider (e.g. Upay, mCash)?**
See [docs/guides/adding_an_mfs_provider.md](guides/adding_an_mfs_provider.md).

**Where does `/time` get its timezone data?**
From `pytz.all_timezones`, matched against the city name you pass by
substring, so `/time dhaka` resolves to `Asia/Dhaka`.

**Can I run this without Docker?**
Yes — `pip install -r requirements.txt && python main.py` after setting
`BOT_TOKEN`. Docker/Render/Railway configs under `deploy/` are optional
convenience, not a requirement.
