# -*- coding: utf-8 -*-

from typing import (
    List,
    Dict,
)
from pathlib import Path

import krait.lib.abc as abc


class DirectoryRenderer(abc.AbstractDirectoryRenderer):
    directories: List[Path]
    root: Path

    def __init__(self, root: Path, *directories: Path):
        super().__init__(root)
        self.directories = list(directories)

    def add_directory(self, directory: Path):
        self.directories.append(directory)

    def add_directories(self, *directories: Path):
        for directory in directories:
            self.directories.append(directory)

    def create_all(self, purge: bool = True):
        self.directories.sort()

        self.root.mkdir()
        for directory in self.directories:
            (self.root / directory).mkdir()

        if purge:
            self.directories = []


class FileRenderer(abc.AbstractFileRenderer):
    files: Dict[str, abc.AbstractFile]

    def __init__(self, root, *files: abc.AbstractFile):
        super().__init__(root)
        self.files = {str(file.path): file for file in files}

    def add_file(self, file: abc.AbstractFile):
        name = str(file.path)

        if name in self.files:
            self.files[name].add_content(file.contents)
        else:
            self.files[name] = file

    def add_files(self, *files: abc.AbstractFile):
        for file in files:
            self.add_file(file)

    def write_all(self, purge: bool = True):
        for file in self.files.values():
            with open(self.root / file.path, 'w') as f:
                f.write(file.contents)

        if purge:
            self.files = {}
