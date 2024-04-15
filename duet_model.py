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
        print('cacca:', klipper_file_info)
        path = klipper_file_info['path'].split('/')
        return DuetFileItem(
            type='d' if len(path) > 1 else 'f',
            name=path[-1],
            size=klipper_file_info['size'],
            date=datetime.fromtimestamp(klipper_file_info['modified']).isoformat()
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
    def from_klipper_file_list(klipper_file_list: KlipperFileList, dir: str = 'gcodes'):
        return DuetFileList(
            dir=dir,
            first=0,
            next=0,
            err=0,
            files=[DuetFileItem.from_klipper_file_info(klipper_file_info) for klipper_file_info in klipper_file_list.result]
        )
