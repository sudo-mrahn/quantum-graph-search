.PHONY: bootstrap test lint clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
FLAKE8_EXCLUDES := .venv,build,dist

bootstrap:
	if [ ! -x "$(PYTHON)" ]; then \
		python3 -m venv $(VENV) || python3 -m virtualenv $(VENV); \
	fi
	$(PIP) install --upgrade pip
	$(PIP) install -e .[test]
	$(PIP) install flake8

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m flake8 . --exclude=$(FLAKE8_EXCLUDES) --count --select=E9,F63,F7,F82 --show-source --statistics
	$(PYTHON) -m flake8 . --exclude=$(FLAKE8_EXCLUDES) --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

clean:
	rm -rf $(VENV)
