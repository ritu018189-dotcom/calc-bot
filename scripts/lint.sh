#!/usr/bin/env bash
set -euo pipefail
python -m py_compile $(find . -name '*.py' -not -path './.venv/*' -not -path './.git/*')
python scripts/check_currency_data.py
black --check .
isort --check-only .
flake8 .
mypy engines mfs_parser
echo "Lint OK"
