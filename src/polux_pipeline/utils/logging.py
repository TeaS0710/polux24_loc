"""Centralised logging utilities for the pipeline."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, Optional


@dataclass(slots=True)
class PipelineLogger:
    """Very small structured logger writing to stdout and an optional CSV file."""

    file_path: Optional[Path] = None

    def _write_csv(self, level: str, message: str, **context: object) -> None:
        if not self.file_path:
            return
        header = ["timestamp", "level", "message", "context"]
        row = [datetime.utcnow().isoformat(), level, message, repr(context)]
        should_write_header = not self.file_path.exists()
        with self.file_path.open("a", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            if should_write_header:
                writer.writerow(header)
            writer.writerow(row)

    def _log(self, level: str, message: str, **context: object) -> None:
        parts = [f"[{level.upper()}]", message]
        if context:
            parts.append(" ".join(f"{key}={value}" for key, value in context.items()))
        print(" ".join(parts))
        self._write_csv(level, message, **context)

    def info(self, message: str, **context: object) -> None:
        self._log("info", message, **context)

    def debug(self, message: str, **context: object) -> None:
        self._log("debug", message, **context)

    def warning(self, message: str, **context: object) -> None:
        self._log("warning", message, **context)

    def error(self, message: str, **context: object) -> None:
        self._log("error", message, **context)


def create_logger(log_path: Path | None) -> PipelineLogger:
    return PipelineLogger(file_path=log_path)


__all__ = ["PipelineLogger", "create_logger"]
