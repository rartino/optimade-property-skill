PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

.PHONY: init deps smoke install-codex install-claude clean

init:
	git submodule update --init --recursive

deps:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install PyYAML

smoke:
	./skills/optimade-property-yaml/scripts/smoke_test.sh

install-codex:
	./install-codex.sh

install-claude:
	./install-claude.sh

clean:
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -prune -exec rm -rf {} +
	find . -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '*.log' \) -delete
	rm -rf tmp build dist
