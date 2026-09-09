#!/usr/bin/env python3
"""
Validates every data/currencies/*.json file has the fields engines/currency_db.py
and the bot's display code expect. Run this after adding/editing a currency file.

Usage: python scripts/check_currency_data.py
"""

import json
import os
import sys

REQUIRED_FIELDS = {"name", "code", "symbol", "country", "flag", "type"}
VALID_TYPES = {"Fiat", "Crypto", "Metal"}

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "currencies"
)


def main():
    errors = []

    for filename in sorted(os.listdir(DATA_DIR)):
        if not filename.endswith(".json"):
            continue
        code = filename[:-5]
        path = os.path.join(DATA_DIR, filename)

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        missing = REQUIRED_FIELDS - data.keys()
        if missing:
            errors.append(f"{filename}: missing fields {sorted(missing)}")

        if data.get("code") != code:
            errors.append(
                f"{filename}: 'code' field ({data.get('code')!r}) doesn't match filename"
            )

        if data.get("type") not in VALID_TYPES:
            errors.append(
                f"{filename}: 'type' must be one of {sorted(VALID_TYPES)}, got {data.get('type')!r}"
            )

    if errors:
        print(f"Found {len(errors)} problem(s):")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print(f"All currency data files OK ({len(os.listdir(DATA_DIR))} files).")


if __name__ == "__main__":
    main()
