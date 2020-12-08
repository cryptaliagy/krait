# -*- coding: utf-8 -*-
'''
Abstract base classes for Krait
'''

from typing import (
    List,
    Union,
    Optional,
)
from pathlib import Path


class AbstractObjectRenderer:
    root: Path

    def __init__(self, root: Path):
        self.root = root


class AbstractFile:
    path: Union[str, Path]
    _contents: List[str]

    def add_content(self, content: str):
        raise NotImplementedError()

    @property
    def contents(self) -> str:
        raise NotImplementedError()


class AbstractFileRenderer(AbstractObjectRenderer):
    def add_file(self, file: AbstractFile):
        raise NotImplementedError()

    def write_all(self):
        raise NotImplementedError()


class AbstractDirectoryRenderer(AbstractObjectRenderer):
    def add_directory(self, directory):
        raise NotImplementedError


class AbstractPlugin:
    project_name: str
    file_renderer: AbstractFileRenderer
    dir_renderer: AbstractDirectoryRenderer

    def __init__(
        self,
        project_name: str,
        file_renderer: AbstractFileRenderer,
        dir_renderer: AbstractDirectoryRenderer,
    ):
        self.project_name = project_name
        self.file_renderer = file_renderer
        self.dir_renderer = dir_renderer

    def render_file(self):
        raise NotImplementedError()


class AbstractVCS(AbstractPlugin):
    pass


class AbstractPythonPlugin(AbstractPlugin):
    packages: List[str]

    def setup_config(self) -> Optional[str]:
        raise NotImplementedError()
