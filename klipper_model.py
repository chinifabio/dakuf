from dataclasses import dataclass
from typing import List

@dataclass
class KlipperFileInfo:
    path: str
    modified: float
    size: int
    permissions: str

@dataclass
class KlipperFileList:
    result: List[KlipperFileInfo]