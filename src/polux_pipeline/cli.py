"""Command line interface for the pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from .commands import FetchCommand, RuleBasedNerCommand
from .config import Settings
from .pipeline import build_environment, run_pipeline
from .utils.files import ensure_parent_directory


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="POLUX pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("input", type=Path, help="JSONL file containing the documents to process")
    common.add_argument("output", type=Path, help="Where to write the processed JSONL file")
    common.add_argument("--log", type=Path, default=None, help="Optional CSV log file")

    fetch_parser = subparsers.add_parser("fetch", parents=[common], help="Fetch raw text from source files")
    fetch_parser.add_argument("--data-root", type=Path, default=Settings().data_root, help="Directory containing source files")

    ner_parser = subparsers.add_parser("ner", parents=[common], help="Run rule-based NER on fetched documents")
    ner_parser.add_argument("--gazetteer", type=Path, default=None, help="Optional plain text file listing locations")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _create_parser()
    args = parser.parse_args(argv)
    settings = Settings()

    if args.command == "fetch":
        settings.data_root = args.data_root
        command = FetchCommand(logger=None, settings=settings)  # type: ignore[arg-type]
    elif args.command == "ner":
        command = RuleBasedNerCommand(logger=None, settings=settings, gazetteer_path=args.gazetteer)  # type: ignore[arg-type]
    else:  # pragma: no cover - safeguarded by argparse
        parser.error(f"Unknown command {args.command}")

    ensure_parent_directory(args.output)
    env = build_environment(command=command, input_path=args.input, output_path=args.output, log_path=args.log)
    run_pipeline(env)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
