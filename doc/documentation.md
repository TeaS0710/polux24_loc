# POLUX Pipeline – Technical Documentation

This document describes the architecture of the modernised POLUX pipeline.

## 1. Overview

The codebase is organised as a lightweight Python package located in `src/polux_pipeline`. Each module targets a single
responsibility so that the overall system is easier to maintain and extend.

```
polux_pipeline/
├── __init__.py
├── __main__.py
├── cli.py
├── commands
│   ├── __init__.py
│   ├── base.py
│   ├── fetch.py
│   └── ner.py
├── config.py
├── models.py
├── ner
│   └── rule_based.py
├── pipeline.py
└── utils
    ├── files.py
    └── logging.py
```

## 2. Data model

`models.Document` is a dataclass capturing four fields: `identifier`, `source_path`, `text`, plus free-form `metadata` and
`annotations`. Conversion helpers `from_dict` and `to_dict` make it easy to convert between JSON representations and the in-memory
object used by the commands.

## 3. Pipeline runner

`pipeline.run_pipeline` streams the input JSONL file, applies the selected command and writes the processed documents to the
output path. All operations are logged through `PipelineLogger`, a CSV-capable structured logger located in `utils.logging`.

## 4. Commands

- `FetchCommand`: resolves disk paths (absolute or relative to `Settings.data_root`) and populates `Document.text` using
  specialised readers for `.txt`, `.md`, `.html` and `.htm` files.
- `RuleBasedNerCommand`: loads a gazetteer (either user provided or from `Settings.gazetteer_locations`) and adds location spans to
  `Document.annotations["locations"]` using the regex-based extractor in `ner.rule_based`.

Each command inherits from `PipelineCommand`, which centralises shared logging behaviour.

## 5. CLI

`cli.py` exposes an `argparse` interface with two subcommands: `fetch` and `ner`. Both accept the input/output paths, an optional
log CSV path and command specific options (`--data-root` for fetch, `--gazetteer` for ner).

Running the CLI module (e.g. `python -m polux_pipeline.cli ner ...`) constructs a `PipelineEnvironment` and delegates to
`run_pipeline`.

## 6. Testing

`tests/test_pipeline.py` contains integration-style unit tests covering both commands. They demonstrate how to instantiate the
commands programmatically, which is also useful for downstream automation.

## 7. Extensibility

Adding a new processing step involves:

1. Creating a new subclass of `PipelineCommand`.
2. Registering it with the CLI (adding a subcommand).
3. Optionally providing tests.

Because the pipeline streams JSONL files, commands remain lightweight and can be composed easily.
