"""
Loads currency/crypto/metal metadata from data/currencies/*.json.

Each file is named after its code (e.g. data/currencies/USD.json) and holds
the display info used by /convert and inline results. Adding support for a
new code is just adding one JSON file here — no code change needed. See
docs/guides/adding_a_currency.md.
"""

import json
import os
from typing import Any, Dict

_DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "currencies"
)


def _load_currency_db(data_dir: str = _DATA_DIR) -> Dict[str, Dict[str, Any]]:
    db: Dict[str, Dict[str, Any]] = {}
    if not os.path.isdir(data_dir):
        return db
    for filename in sorted(os.listdir(data_dir)):
        if not filename.endswith(".json"):
            continue
        code = filename[:-5]
        with open(os.path.join(data_dir, filename), encoding="utf-8") as f:
            db[code] = json.load(f)
    return db


CURRENCY_DB = _load_currency_db()


def get_currency(code: str) -> Dict[str, Any]:
    """Look up a currency by code, falling back to a generic placeholder."""
    return CURRENCY_DB.get(code.upper(), {"flag": "🏳️", "name": code, "code": code})
