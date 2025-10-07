"""Base command interfaces."""

from __future__ import annotations

from dataclasses import dataclass
from ..models import Document
from ..utils.logging import PipelineLogger


@dataclass(slots=True, kw_only=True)
class PipelineCommand:
    """Base class for pipeline commands."""

    logger: PipelineLogger | None = None
    name: str = "command"

    def prepare(self) -> None:  # pragma: no cover - default implementation
        if self.logger:
            self.logger.debug("Preparing command", command=self.name)

    def process(self, document: Document) -> Document:  # pragma: no cover - abstract method
        raise NotImplementedError

    def finalize(self) -> None:  # pragma: no cover - default implementation
        if self.logger:
            self.logger.debug("Finalizing command", command=self.name)
