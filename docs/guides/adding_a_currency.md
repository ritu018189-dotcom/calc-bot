# Adding a currency

Currency metadata lives as one JSON file per code under `data/currencies/`,
loaded automatically by `engines/currency_db.py` at import time — no code
change needed.

1. Create `data/currencies/<CODE>.json`:

   ```json
   {
     "name": "Example Currency",
     "code": "XYZ",
     "symbol": "X$",
     "country": "Example Country",
     "flag": "🏳️",
     "type": "Fiat"
   }
   ```

2. `type` is one of `"Fiat"`, `"Crypto"`, or `"Metal"` — it's informational
   only (used for display), not enforced anywhere.
3. That's it. `/convert` and inline currency queries will pick it up the
   next time the bot starts. Note that `/convert` still needs Yahoo Finance
   to actually quote a rate for the pair (`<CODE1><CODE2>=X` or
   `<CODE1>-<CODE2>`); adding the JSON file only controls how it's *displayed*
   (flag, name), not whether a live rate exists for it.
4. Add a quick assertion to `tests/unit/test_currency_db.py` if the currency
   is significant enough to guard against accidental deletion.
