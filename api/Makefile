install:
	pip install -r requirements.txt

dev:
	python -m fastapi_cli dev

prod:
	python -m fastapi_cli run

check: lint typecheck

lint:
	python -m ruff check

format:
	python -m ruff format

typecheck:
	python -m mypy .

update-openapi:
	python -m scripts.gen-openapi > openapi.json

tests: unit-tests bruno-tests

unit-tests:

bruno-tests:
	python -m scripts.run-tests
