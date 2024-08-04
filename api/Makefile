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
	python gen-openapi.py > ../openapi.json
