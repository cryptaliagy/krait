# -*- coding: utf-8 -*-
import krait.lib.abc as abc
import krait.lib.files as kf

from git import Repo  # type: ignore
from pathlib import Path
from typing import Any

from krait.utils.templates import get_env


class BaseVCSPlugin(abc.AbstractVCS):
    name: str
    ignore_file: kf.File

    def __init__(
        self,
        project_name: str,
        file_renderer: abc.AbstractFileRenderer,
        dir_renderer: abc.AbstractDirectoryRenderer
    ):
        super().__init__(project_name, file_renderer, dir_renderer)
        self.name = ''
        self.env = get_env()

    def initialize(self, project_path: Path):
        self.dir_renderer.output(f'Initializing {self.name} repository...')

    def render_ignorefile(self, ignore_file_name: str, **render_params: Any):
        self.file_renderer.output(f'Adding {ignore_file_name}...')
        self.ignore_file = kf.File(ignore_file_name)
        contents = self.env.get_template(f'{ignore_file_name}.jinja2').render(**render_params)
        self.ignore_file.add_content(contents)
        self.file_renderer.add_file(self.ignore_file)


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
        self.render_ignorefile('.gitignore')


class NoVCS(BaseVCSPlugin):
    def initialize(self, project_path: Path):
        pass
