.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help install test coverage run

help:
	@echo "Available targets:"
	@echo "  install   - Create .venv and install requirements"
	@echo "  test      - Run test suite (uses scripts/test.sh)"
	@echo "  coverage  - Run tests with coverage (scripts/coverage.sh)"
	@echo "  run       - Run API locally (python app.py)"

install:
	python3 -m venv .venv ; \
	. .venv/bin/activate ; \
	pip install -r requirements.txt

test:
	chmod +x scripts/test.sh ; \
	./scripts/test.sh

coverage:
	chmod +x scripts/coverage.sh ; \
	./scripts/coverage.sh

run:
	. .venv/bin/activate ; \
	python app.py


