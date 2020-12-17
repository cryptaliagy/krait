# -*- coding: utf-8 -*-
import krait.lib.abc as abc
from git import Repo  # type: ignore
from pathlib import Path


class BaseVCSPlugin(abc.AbstractVCS):
    name: str

    def __init__(
        self,
        project_name: str,
        file_renderer: abc.AbstractFileRenderer,
        dir_renderer: abc.AbstractDirectoryRenderer
    ):
        super().__init__(project_name, file_renderer, dir_renderer)
        self.name = ''

    def initialize(self, project_path: Path):
        self.file_renderer.output(f'Initializing {self.name} repository...')


class GitPlugin(BaseVCSPlugin):
    repository: Repo

    def __init__(
        self,
        project_name: str,
        file_renderer: abc.AbstractFileRenderer,
        dir_renderer: abc.AbstractDirectoryRenderer
    ):
        super().__init__(project_name, file_renderer, dir_renderer)
        self.name = 'git'

    def initialize(self, project_path: Path):
        super().initialize(project_path)
        self.repository = Repo.init(project_path.resolve(), mkdir=False)


class NoVCS(BaseVCSPlugin):
    def initialize(self, project_path: Path):
        pass
