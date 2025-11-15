# Simple Makefile for common developer tasks
# - clean: remove temporary/build files and caches
# - migrate: run alembic migrations (uses 'uv' if available)

.PHONY: help clean clean-pyc clean-all migrate

SHELL := /bin/bash

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  clean        Remove __pycache__, .pyc files, pytest/mypy caches, build artifacts"
	@echo "  clean-pyc    Remove only python cache files (__pycache__, *.pyc)"
	@echo "  clean-all    Remove everything from clean + .venv (only if CLEAN_VENV=true)"
	@echo "  migrate      Run alembic migrations (uses 'uv' if available; falls back to 'alembic')"

# detect migration command: prefer 'uv' if on path
MIGRATE := $(shell if command -v uv >/dev/null 2>&1; then echo "uv run alembic"; else echo "alembic"; fi)

clean-pyc:
	@echo "Removing Python cache files..."
	@find . -type d -name "__pycache__" -print -exec rm -rf {} + || true
	@find . -name "*.pyc" -print -delete || true

clean:
	@$(MAKE) clean-pyc
	@echo "Removing test/build caches and artifacts..."
	@rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build *.egg-info || true

clean-all: clean
	@if [ "$(CLEAN_VENV)" = "true" ]; then \
		echo "Removing .venv ..."; \
		rm -rf .venv || true; \
	else \
		echo "Skipping .venv removal (set CLEAN_VENV=true to remove)"; \
	fi

migrate:
	@echo "Running migrations using: $(MIGRATE)"
	@$(MIGRATE) upgrade head
