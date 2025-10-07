"""Utility helpers for working with files."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path


class _HTMLStripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self._chunks.append(data.strip())

    def get_data(self) -> str:
        return " ".join(self._chunks)


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_html_file(path: Path) -> str:
    parser = _HTMLStripper()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.get_data()


def ensure_parent_directory(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
