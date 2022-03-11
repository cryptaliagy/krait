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
        self._output = None

    def set_output(self, output):
        self._output = output

    def output(self, msg: str):
        if self._output is not None:
            self._output(msg)


class AbstractFile:
    path: Union[str, Path]
    _contents: List[str]
    executable: bool

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
    vcs: 'AbstractVCS'

    def add_directory(self, directory):
        raise NotImplementedError

    def attach_vcs(self, vcs: 'AbstractVCS'):
        self.vcs = vcs


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

    def make_targets(self) -> Optional[str]:
        raise NotImplementedError()


class AbstractVCS(AbstractPlugin):
    def initialize(self, project_path: Path):
        pass


class AbstractPythonPlugin(AbstractPlugin):
    packages: List[str]

    def setup_config(self) -> Optional[str]:
        raise NotImplementedError()


class AbstractPythonProjectFramework(AbstractPythonPlugin):
    project_type: str
