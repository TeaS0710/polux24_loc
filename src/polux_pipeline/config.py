"""Project configuration helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass(slots=True)
class Settings:
    """Application level configuration.

    Parameters
    ----------
    data_root:
        Base directory where source files are located.
    output_root:
        Default directory where pipeline outputs are written.
    gazetteer_locations:
        Optional iterable of location names to seed the NER dictionary.
    """

    data_root: Path = Path("data/source")
    output_root: Path = Path("data/processed")
    gazetteer_locations: Iterable[str] = field(default_factory=lambda: ("Paris", "Marseille", "Lyon", "France"))

    def resolve_data_path(self, relative_path: str | Path) -> Path:
        """Return the absolute path for a file located under ``data_root``."""

        candidate = Path(relative_path)
        if candidate.is_absolute():
            return candidate
        return (self.data_root / candidate).resolve()

    def ensure_output_directory(self, folder: str | Path) -> Path:
        """Create a directory for pipeline outputs if necessary."""

        path = (self.output_root / folder).resolve()
        path.mkdir(parents=True, exist_ok=True)
        return path
