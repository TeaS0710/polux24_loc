"""Simple rule based location extractor."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, List

_LOCATION_PATTERN = re.compile(r"\b([A-Z][a-zA-Z\-']+(?:\s+[A-Z][a-zA-Z\-']+)*)\b")


@dataclass(slots=True)
class RuleBasedExtractor:
    gazetteer: Iterable[str]
    _dictionary: dict[str, str] = field(init=False, repr=False, default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_dictionary", {entry.lower(): entry for entry in self.gazetteer})

    def extract(self, text: str) -> List[dict]:
        matches = []
        if not text:
            return matches
        for match in _LOCATION_PATTERN.finditer(text):
            candidate = match.group(1)
            if candidate.lower() in self._dictionary:
                matches.append({"text": candidate, "start": match.start(1), "end": match.end(1)})
        return matches
