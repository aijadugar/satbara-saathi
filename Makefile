.PHONY: dev test lint clean docker-build docker-run

PYTHON  := python3
PYTEST  := pytest

dev:
	$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	$(PYTEST) -v --cov=app --cov-report=term-missing

lint:
	$(PYTHON) -m ruff check app/ tests/

clean:
	rm -rf .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t satbara-saathi .

docker-run:
	docker run -p 8000:8000 --env-file .env satbara-saathi
