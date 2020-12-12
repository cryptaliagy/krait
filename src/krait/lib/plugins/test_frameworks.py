# -*- coding: utf-8 -*-
'''
Test frameworks used for Krait
'''

import krait.lib.plugins.base_plugin as bp
import krait.lib.plugins.project_frameworks as pf
import krait.lib.renderers as rndr
import krait.lib.files as kf

from typing import (
    List,
    Optional,
)
from pathlib import Path


class BaseTestFramework(bp.BasePythonPlugin):
    project_framework: pf.BaseProjectFramework

    def __init__(
        self,
        project_name: str,
        project_framework: pf.BaseProjectFramework,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):

        super().__init__(project_name, file_renderer, dir_renderer)
        self.project_framework = project_framework
        self.name = ''
        self.rendering_params = {'project_name': project_name}
        dir_renderer.add_directory(Path('tests'))
        file_renderer.add_file(kf.File('tests/__init__.py'))


class Pytest(BaseTestFramework):
    packages = ['pytest', 'pytest-cov']

    def __init__(
        self,
        project_name: str,
        project_framework: pf.BaseProjectFramework,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        super().__init__(project_name, project_framework, file_renderer, dir_renderer)
        self.name = f'pytest-{self.project_framework.name}'
        self.setup_name = 'pytest'
        self.setup_vars = {'project_framework': project_framework.name}
        self.file_location = 'tests'
        self.file_name = project_framework.test_file


class NoTesting(BaseTestFramework):
    packages: List[str] = []

    def __init__(self, *args):
        pass

    def render_file(self):
        pass

    def setup_config(self) -> Optional[str]:
        return None
