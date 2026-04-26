.PHONY: lint test run-api

lint:
	uv run ruff check src tests
	uv run mypy src

test:
	uv run pytest -q

run-api:
	uv run uvicorn g2p_modern.api.main:app --reload --app-dir src
