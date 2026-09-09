#!/usr/bin/env python3
"""
Regenerates nothing on its own — this is the reference generator used once
to seed data/currencies/*.json from a Python dict. Kept so the provenance of
the data files is auditable and so a bulk update (e.g. re-flagging every
entry's `type`) can be scripted instead of hand-edited 170+ times.

Usage:
    python scripts/gen_currency_data.py path/to/source_dict.py
        (a .py file that defines CURRENCY_DB = {...})
"""

import importlib.util
import json
import os
import sys


def load_source_dict(path: str) -> dict:
    spec = importlib.util.spec_from_file_location("currency_source", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.CURRENCY_DB


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    source_path = sys.argv[1]
    currency_db = load_source_dict(source_path)

    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "currencies",
    )
    os.makedirs(out_dir, exist_ok=True)

    for code, info in currency_db.items():
        with open(os.path.join(out_dir, f"{code}.json"), "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
            f.write("\n")

    print(f"Wrote {len(currency_db)} files to {out_dir}")


if __name__ == "__main__":
    main()
