install:
	pip install -r requirements.txt

dev:
	python -m fastapi_cli dev

prod:
	python -m fastapi_cli prod

check: lint typecheck

lint:
	python -m ruff check

format:
	python -m ruff format

typecheck:
	python -m mypy .
