# -*- coding: utf-8 -*-

from typing import (
    List,
    Dict,
    Union,
    Optional,
)
from pathlib import Path

import krait.lib.abc as abc
from krait.utils.templates import env


class DirectoryRenderer(abc.AbstractDirectoryRenderer):
    directories: List[Path]
    root: Path

    def __init__(self, root: Path, *directories: Path):
        super().__init__(root)
        self.directories = list(directories)

    def add_directories(self, directory: Path):
        self.directories.append(directory)

    def create_all(self, purge: bool = True):
        self.directories.sort()

        self.root.mkdir()
        for directory in self.directories:
            (self.root / directory).mkdir()

        if purge:
            self.directories = []


class File:
    path: Union[str, Path]
    _contents: List[str]

    def __init__(self, path: Union[str, Path], *contents: str):
        self.path = path
        self._contents = list(contents)

    def add_content(self, content: str):
        self._contents.append(content)

    @property
    def contents(self) -> str:
        return '\n'.join(self._contents)


class SetupScript(File):
    def __init__(
        self,
        project_name: str,
        author: str,
        author_email: str,
        cli_framework: Optional[abc.AbstractCliFramework],
        linter: Optional[abc.AbstractLinter],
        type_checker: Optional[abc.AbstractTypeChecker],
        test_framework: Optional[abc.AbstractTestFramework]
    ):
        self.path = 'setup.py'
        self.author = author
        self.author_email = author_email
        self.project_name = project_name
        self.cli_framework = cli_framework
        self.linter = linter
        self.type_checker = type_checker
        self.test_framework = test_framework
        self.dependencies = set()
        self.test_dependencies = set()

        if self.cli_framework:
            self.dependencies.update(self.cli_framework.packages)

        if self.linter:
            self.test_dependencies.update(self.linter.packages)

        if self.type_checker:
            self.test_dependencies.update(self.type_checker.packages)

        if self.test_framework:
            self.test_dependencies.update(self.test_framework.packages)

    @property
    def contents(self) -> str:
        setup_template = env.get_template('setup.py.jinja2')
        return setup_template.render(
            project_name=self.project_name,
            author=self.author,
            author_email=self.author_email,
            install_dependencies=[*self.dependencies],
            test_dependencies=[*self.test_dependencies]
        ) + '\n'


class FileRenderer(abc.AbstractFileRenderer):
    files: Dict[str, File]

    def __init__(self, root, *files: File):
        super().__init__(root)
        self.files = {str(file.path): file for file in files}

    def add_file(self, file: File):
        name = str(file.path)

        if name in self.files:
            self.files[name].add_content(file.contents)
        else:
            self.files[name] = file

    def write_all(self, purge: bool = True):
        for file in self.files.values():
            with open(self.root / file.path, 'w') as f:
                f.write(file.contents)

        if purge:
            self.files = {}
