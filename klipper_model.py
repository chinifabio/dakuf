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
    
    def generate_tree(self):
        tree = {}
        for file in self.result:
            path = file['path'].split('/')
            current = tree
            for part in path[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[path[-1]] = KlipperFileInfo(**file)
        return tree