from dataclasses import dataclass
from typing import List
from datetime import datetime

from klipper_model import KlipperFileInfo, KlipperFileList

@dataclass
class DuetFileItem:
    type: str
    name: str
    size: int
    date: str

    @staticmethod
    def from_klipper_file_info(klipper_file_info: KlipperFileInfo):
        klipper_path = klipper_file_info.path.split('/')
        return DuetFileItem(
            type='f',
            name=klipper_path[-1],
            size=klipper_file_info.size,
            date=datetime.fromtimestamp(klipper_file_info.modified).isoformat()
        )

@dataclass
class DuetFileList:
    dir: str
    first: int
    next: int
    """
    0: List query successful
    1: Drive is not mounted
    2: Directory does not exist
    """
    err: int
    files: List[DuetFileItem]

    @staticmethod
    def from_klipper_tree(klipper_tree: dict, dir: str = 'gcodes'):
        dir_parts = dir.split('/')
        root = dir_parts[0]
        path = dir_parts[1:] if len(dir_parts) > 1 else []
        try:
            for part in path:
                klipper_tree = klipper_tree[part]
        except KeyError:
            return DuetFileList(
                dir=dir,
                first=0,
                next=0,
                err=2,
                files=[]
            )
        files = []
        for key, value in klipper_tree.items():
            print(type(value))
            if isinstance(value, KlipperFileInfo):
                files.append(DuetFileItem.from_klipper_file_info(value))
            else:
                files.append(DuetFileItem(
                    type='d',
                    name=key,
                    size=0,
                    date=''
                ))
        return DuetFileList(
            dir=dir,
            first=0,
            next=0,
            err=0,
            files=files
        )
