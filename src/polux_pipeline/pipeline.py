"""Streaming pipeline runner."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Protocol

from .models import Document
from .utils.logging import PipelineLogger, create_logger


class Command(Protocol):
    """Protocol for commands able to process documents."""

    name: str

    def prepare(self) -> None: ...

    def process(self, document: Document) -> Document: ...

    def finalize(self) -> None: ...


@dataclass(slots=True)
class PipelineEnvironment:
    command: Command
    input_path: Path
    output_path: Path
    logger: PipelineLogger


def load_documents(input_path: Path) -> Iterator[Document]:
    with input_path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
            yield Document.from_dict(payload)


def write_document(output_path: Path, document: Document) -> None:
    with output_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(document.to_dict(), ensure_ascii=False) + "\n")


def run_pipeline(env: PipelineEnvironment) -> None:
    env.logger.info("Starting pipeline", command=env.command.name)
    env.command.prepare()
    processed = 0
    env.output_path.parent.mkdir(parents=True, exist_ok=True)
    env.output_path.write_text("", encoding="utf-8")
    for document in load_documents(env.input_path):
        env.logger.debug("Processing document", document_id=document.identifier)
        updated = env.command.process(document)
        write_document(env.output_path, updated)
        processed += 1
    env.command.finalize()
    env.logger.info("Pipeline completed", processed=processed, output=str(env.output_path))


def build_environment(*, command: Command, input_path: Path, output_path: Path, log_path: Path | None = None) -> PipelineEnvironment:
    logger = create_logger(log_path)
    if hasattr(command, "logger"):
        command.logger = logger  # type: ignore[attr-defined]
    return PipelineEnvironment(command=command, input_path=input_path, output_path=output_path, logger=logger)


__all__ = ["PipelineEnvironment", "run_pipeline", "build_environment"]
