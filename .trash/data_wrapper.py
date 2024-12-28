from dataclasses import dataclass
from typing import ClassVar
import msgpack

from utils.TextExtractor import get_text, extractors


class DataWrapper:
  def __init__(self):
    pass
  
  def encode(self):
    msgpack.packb(vars(self), use_bin_type=True)

  @classmethod
  def decode(cls, data):
    return cls(**msgpack.unpackb(data, raw=False))
    

@dataclass(frozen=True, slots=True)
class Document(DataWrapper):
  supported_exts: ClassVar[set] = set(extractors.keys())
  
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


@dataclass(frozen=True, slots=True)
class LocEntity(DataWrapper):
  document: str
  end: int
  motor: str
  start: int
  text: str
