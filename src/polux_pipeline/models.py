"""Core data models used by the pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, MutableMapping


@dataclass(slots=True)
class Document:
    """Representation of an item flowing through the pipeline."""

    identifier: str
    source_path: Path | None = None
    text: str = ""
    metadata: MutableMapping[str, Any] = field(default_factory=dict)
    annotations: MutableMapping[str, Any] = field(default_factory=lambda: {"locations": []})

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Document":
        identifier = str(payload.get("id") or payload.get("identifier") or payload.get("name"))
        if not identifier:
            raise ValueError("Document payload must contain an 'id' or 'identifier' field")

        metadata = {key: value for key, value in payload.items() if key not in {"id", "identifier", "name", "text", "annotations", "source_path"}}
        source_value = payload.get("source_path") or payload.get("file_path") or metadata.get("file_path")
        source_path = Path(source_value) if source_value else None
        text = payload.get("text", "")
        annotations = payload.get("annotations") or {"locations": []}
        return cls(identifier=identifier, source_path=source_path, text=text, metadata=metadata, annotations=annotations)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.identifier,
            "source_path": str(self.source_path) if self.source_path else None,
            "text": self.text,
            "metadata": dict(self.metadata),
            "annotations": self._serialise_annotations(),
        }

    def _serialise_annotations(self) -> Dict[str, Any]:
        output = {}
        for key, value in self.annotations.items():
            if isinstance(value, Path):
                output[key] = str(value)
            elif isinstance(value, Iterable) and not isinstance(value, (str, bytes, dict)):
                output[key] = list(value)
            else:
                output[key] = value
        return output

    def add_locations(self, locations: Iterable[Dict[str, Any]]) -> None:
        bucket = self.annotations.setdefault("locations", [])
        bucket.extend(locations)


__all__ = ["Document"]
