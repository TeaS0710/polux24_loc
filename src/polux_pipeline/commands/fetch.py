"""Command that fills ``Document.text`` based on disk files."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar
from pathlib import Path
from typing import Callable

from ..config import Settings
from ..models import Document
from ..utils.files import read_html_file, read_text_file
from ..utils.logging import PipelineLogger
from .base import PipelineCommand


@dataclass(slots=True, kw_only=True)
class FetchCommand(PipelineCommand):
    settings: Settings | None = None
    _reader_by_suffix: dict[str, Callable[[Path], str]] = field(init=False, repr=False, default_factory=dict)
    name: ClassVar[str] = "fetch"

    def prepare(self) -> None:
        PipelineCommand.prepare(self)
        self._reader_by_suffix = {
            ".txt": read_text_file,
            ".md": read_text_file,
            ".html": read_html_file,
            ".htm": read_html_file,
        }

    def _resolve_source(self, document: Document) -> Path:
        if document.source_path:
            path = document.source_path
        else:
            source_hint = document.metadata.get("source") or document.metadata.get("file_path")
            if not source_hint:
                raise FileNotFoundError(f"Document {document.identifier} does not contain a source path")
            path = Path(source_hint)

        if not path.is_absolute() and self.settings:
            path = self.settings.resolve_data_path(path)
        return path

    def process(self, document: Document) -> Document:
        path = self._resolve_source(document)
        suffix = path.suffix.lower()
        reader = self._reader_by_suffix.get(suffix)
        if reader is None:
            raise ValueError(f"Unsupported file type '{suffix}' for document {document.identifier}")
        if self.logger:
            self.logger.debug("Reading file", path=str(path))
        document.text = reader(path)
        document.metadata["source_path"] = str(path)
        return document

