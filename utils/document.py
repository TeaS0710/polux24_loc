from dataclasses import dataclass

from base import DataWrapper
from text_extractor import get_text

@dataclass(frozen=True, slots=True)
class Document(DataWrapper):
  author: str
  group: str
  text: str
  url: str

  @classmethod
  def from_file(cls, author, group, path, url):
    return cls(
      author=author,
      group=group,
      text=get_text(path),
      url=url
    )
