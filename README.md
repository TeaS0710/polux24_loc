# POLUX Pipeline

Modern, maintainable pipeline for working with the POLUX corpus. This rewrite replaces the legacy prototype with a compact and
reliable toolkit composed of small, testable scripts.

## Features

- **Streaming JSONL processing** – documents are read and written line by line.
- **Modular commands** – `fetch` loads raw text from files, `ner` applies a lightweight location detector.
- **Rule-based NER** – a small gazetteer backed by a regex matcher that can be extended with your own vocabulary.
- **Structured logging** – optional CSV logs capture each pipeline step.
- **Makefile workflow** – consistent entry points for installation, testing and running commands.

## Installation

```bash
python3 -m pip install -e .
```

The project targets Python 3.10+.

## Usage

The CLI exposes two subcommands. Both operate on JSON Lines (`.jsonl`) documents with at least an `id` field.

### Fetch raw text

```bash
python -m polux_pipeline.cli fetch INPUT.jsonl OUTPUT.jsonl --data-root data/source
```

Each JSON object should contain either a `source_path` or a metadata key named `source`/`file_path` that points to the file to
read.

### Run rule-based NER

```bash
python -m polux_pipeline.cli ner INPUT.jsonl OUTPUT.jsonl --gazetteer data/locations.txt
```

The gazetteer file is optional. Without it, a small default dictionary (Paris, Marseille, Lyon, France) is used.

### Logging

Use the `--log` option on any command to generate a CSV trace of pipeline operations.

```bash
python -m polux_pipeline.cli fetch INPUT.jsonl OUTPUT.jsonl --log logs/pipeline.csv
```

## Development

Useful commands are available through the `Makefile`:

```bash
make install
make test
make run-fetch ARGS="input.jsonl output.jsonl"
```

The tests can be executed via `make test` or `pytest` directly.

## Project layout

```
polux24_loc/
├── Makefile
├── pyproject.toml
├── src/
│   └── polux_pipeline/
│       ├── commands/
│       ├── ner/
│       ├── utils/
│       └── ...
└── tests/
```

## License

MIT License © 2024 POLUX Team
