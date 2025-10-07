from pathlib import Path
import json

from polux_pipeline.commands.fetch import FetchCommand
from polux_pipeline.commands.ner import RuleBasedNerCommand
from polux_pipeline.config import Settings
from polux_pipeline.pipeline import build_environment, run_pipeline


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def test_fetch_pipeline(tmp_path: Path) -> None:
    source = tmp_path / "data" / "doc.txt"
    source.parent.mkdir(parents=True)
    source.write_text("Bonjour Paris", encoding="utf-8")

    input_path = tmp_path / "input.jsonl"
    write_jsonl(input_path, [{"id": "doc1", "source_path": str(source)}])

    output_path = tmp_path / "output.jsonl"
    env = build_environment(
        command=FetchCommand(logger=None, settings=Settings()),
        input_path=input_path,
        output_path=output_path,
        log_path=None,
    )
    run_pipeline(env)

    records = read_jsonl(output_path)
    assert records[0]["text"] == "Bonjour Paris"


def test_ner_pipeline(tmp_path: Path) -> None:
    input_path = tmp_path / "input.jsonl"
    write_jsonl(input_path, [{"id": "doc1", "text": "Nous visitons Lyon et Paris."}])

    output_path = tmp_path / "output.jsonl"
    env = build_environment(
        command=RuleBasedNerCommand(logger=None, settings=Settings()),
        input_path=input_path,
        output_path=output_path,
        log_path=None,
    )
    run_pipeline(env)

    records = read_jsonl(output_path)
    locations = records[0]["annotations"]["locations"]
    assert any(entry["text"] == "Lyon" for entry in locations)
    assert any(entry["text"] == "Paris" for entry in locations)
