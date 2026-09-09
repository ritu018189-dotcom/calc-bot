#!/usr/bin/env bash
set -euo pipefail
pip install -q -r requirements.txt -r requirements-dev.txt
pytest "$@"
