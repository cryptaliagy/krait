# -*- coding: utf-8 -*-

from typing import (
    List,
    Dict,
    Union,
)
from pathlib import Path


class DirectoryRenderer:
    directories: List[Path]

    def __init__(self, *directories: Path):
        self.directories = list(directories)

    def add_directories(self, directory: Path):
        self.directories.append(directory)

    def create_all(self, purge: bool = True):
        self.directories.sort()

        for directory in self.directories:
            directory.mkdir()

        if purge:
            self.directories = []


class File:
    path: Union[str, Path]
    _contents: List[str]

    def __init__(self, path: Union[str, Path]):
        self.path = path
        self._contents = []

    def add_content(self, content: str):
        self._contents.append(content)

    @property
    def contents(self) -> str:
        return '\n'.join(self._contents)


class FileRenderer:
    files: Dict[str, File]

    def __init__(self, *files: File):
        self.files = {str(file.path): file for file in files}

    def add_file(self, file: File):
        name = str(file.path)

        if name in self.files:
            self.files[name].add_content(file.contents)
        else:
            self.files[name] = file

    def write_all(self, purge: bool = True):
        for file in self.files.values():
            with open(file.path, 'w') as f:
                f.write(file.contents)

        if purge:
            self.files = {}
