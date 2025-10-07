.PHONY: install format lint test run-fetch run-ner clean

PYTHON = python3
PIP = $(PYTHON) -m pip

install:
$(PIP) install -e .

format:
$(PYTHON) -m black src tests

lint:
$(PYTHON) -m ruff check src tests

test:
$(PYTHON) -m pytest

run-fetch:
$(PYTHON) -m polux_pipeline.cli fetch $(ARGS)

run-ner:
$(PYTHON) -m polux_pipeline.cli ner $(ARGS)

clean:
rm -rf build dist *.egg-info .pytest_cache
