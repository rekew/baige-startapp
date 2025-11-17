.PHONY: help install db-init db-migrate db-upgrade db-downgrade run clean

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make db-init       - Initialize alembic"
	@echo "  make db-migrate    - Create new migration"
	@echo "  make db-upgrade    - Apply migrations"
	@echo "  make db-downgrade  - Rollback last migration"
	@echo "  make run           - Run FastAPI server"
	@echo "  make clean         - Remove cache files"

install:
	pip install -r backend/requirements.txt

db-init:
	alembic init alembic

db-migrate:
	alembic revision --autogenerate -m "$(message)"

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

run:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8008

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete