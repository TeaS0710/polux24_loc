"""Command that performs a lightweight rule-based NER."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Iterable, List

from ..config import Settings
from ..models import Document
from ..ner.rule_based import RuleBasedExtractor
from ..utils.logging import PipelineLogger
from .base import PipelineCommand


@dataclass(slots=True, kw_only=True)
class RuleBasedNerCommand(PipelineCommand):
    settings: Settings
    gazetteer_path: Path | None = None
    _extractor: RuleBasedExtractor | None = field(init=False, repr=False, default=None)
    name: ClassVar[str] = "ner"

    def prepare(self) -> None:
        PipelineCommand.prepare(self)
        if self.gazetteer_path:
            entries = self._load_gazetteer(self.gazetteer_path)
        else:
            entries = list(self.settings.gazetteer_locations)
        self._extractor = RuleBasedExtractor(entries)
        if self.logger:
            self.logger.debug("NER command ready", entries=len(entries))

    def _load_gazetteer(self, path: Path) -> List[str]:
        with path.open("r", encoding="utf-8") as stream:
            return [line.strip() for line in stream if line.strip() and not line.startswith("#")]

    def process(self, document: Document) -> Document:
        if self._extractor is None:
            raise RuntimeError("NER command used before preparation")
        matches = self._extractor.extract(document.text)
        document.add_locations(matches)
        if self.logger:
            self.logger.debug("Locations extracted", document_id=document.identifier, count=len(matches))
        return document
