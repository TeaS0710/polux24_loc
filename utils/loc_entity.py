from dataclasses import dataclass

from base import DataWrapper

@dataclass
class LocEntity(DataWrapper):
  document: str
  end: int
  motor: str
  start: int
  text: str
