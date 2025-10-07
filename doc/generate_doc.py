"""Regenerate the technical documentation."""

from __future__ import annotations

from pathlib import Path

DOC_PATH = Path(__file__).with_name("documentation.md")
PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "src" / "polux_pipeline"


def build_tree(root: Path, prefix: str = "") -> list[str]:
    entries = sorted([entry for entry in root.iterdir() if not entry.name.startswith("__pycache__")])
    lines: list[str] = []
    for index, entry in enumerate(entries):
        connector = "└──" if index == len(entries) - 1 else "├──"
        lines.append(f"{prefix}{connector} {entry.name}")
        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            lines.extend(build_tree(entry, prefix + extension))
    return lines


def regenerate_documentation() -> None:
    tree_block = "\n".join(["```", "polux_pipeline/"] + build_tree(PACKAGE_ROOT) + ["```"])
    content = DOC_PATH.read_text(encoding="utf-8")
    start = content.find("```")
    if start == -1:
        raise RuntimeError("documentation.md is missing the project tree code block")
    end = content.find("```", start + 3)
    if end == -1:
        raise RuntimeError("documentation.md code block is not terminated")
    end += 3
    new_content = content[:start] + tree_block + content[end:]
    DOC_PATH.write_text(new_content, encoding="utf-8")


if __name__ == "__main__":
    regenerate_documentation()
