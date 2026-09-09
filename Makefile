.PHONY: install test lint format run

install:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest

lint:
	bash scripts/lint.sh

format:
	bash scripts/format.sh

run:
	python main.py
