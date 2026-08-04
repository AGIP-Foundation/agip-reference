.PHONY: install test lint format typecheck check clean

PYTHON ?= python3

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format .

typecheck:
	$(PYTHON) -m mypy src

check: lint typecheck test

clean:
	rm -rf .coverage .mypy_cache .pytest_cache .ruff_cache htmlcov build dist
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
