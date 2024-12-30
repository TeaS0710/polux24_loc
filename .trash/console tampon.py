from rich.console import Console
from rich.text import Text
import json

def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_text_from_file(path, text_id, logger):
    with FileManager(path, "r", logger) as reader:
        return reader.read(text_id)

def format_text_with_indices(text, indices):
    rich_text = Text()
    last_end = 0

    for start, end in indices:
        rich_text.append(text[last_end:start])
        rich_text.append(text[start:end], style="bold red")
        last_end = end

    rich_text.append(text[last_end:])
    return rich_text

def main(text_id, path, logger):
    console = Console()
    data = load_data(path)

    if text_id not in data:
        logger.error(f"Text ID {text_id} not found in {path}")
        return

    indices = data[text_id]
    text = read_text_from_file(path, text_id, logger)
    rich_text = format_text_with_indices(text, indices)
    console.print(rich_text)

main("text_id", "data.json", logger)
