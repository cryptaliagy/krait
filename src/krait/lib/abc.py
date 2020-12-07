# -*- coding: utf-8 -*-
'''
Abstract base classes for Krait
'''

from typing import (
    Dict,
    List,
)
from pathlib import Path


class AbstractPlugin:
    project_name: str

    def __init__(self, project_name: str):
        self.project_name = project_name


class AbstractObjectRenderer:
    root: Path

    def __init__(self, root: Path):
        self.root = root


class AbstractFileRenderer(AbstractObjectRenderer):
    def add_file(self, file):
        raise NotImplementedError()

    @property
    def contents(self) -> str:
        raise NotImplementedError()


class AbstractDirectoryRenderer(AbstractObjectRenderer):
    def add_directory(self, directory):
        raise NotImplementedError


class AbstractVCS(AbstractPlugin):
    pass


class AbstractPythonPlugin(AbstractPlugin):
    packages: List[str]
    file_renderer: AbstractFileRenderer
    dir_renderer: AbstractDirectoryRenderer

    def __init__(
        self,
        project_name: str,
        file_renderer: AbstractFileRenderer,
        dir_renderer: AbstractDirectoryRenderer,
    ):
        super().__init__(project_name)
        self.file_renderer = file_renderer
        self.dir_renderer = dir_renderer


class AbstractCliFramework(AbstractPythonPlugin):
    def render_file(self) -> None:
        '''
        Render the main.py file and inserts it into the file renderer
        '''
        raise NotImplementedError()


class AbstractLinter(AbstractPythonPlugin):
    configurations: Dict[str, str]


class AbstractTypeChecker(AbstractPythonPlugin):
    pass


class AbstractTestFramework(AbstractPythonPlugin):
    pass


class AbstractAutomation(AbstractPythonPlugin):
    linter: str
    type_checker: str
    test_framework: str
