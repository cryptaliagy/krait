# -*- coding: utf-8 -*-
'''
Test frameworks used for Krait
'''

import krait.lib.plugins.base_plugin as bp
import krait.lib.renderers as rndr
import krait.lib.files as kf

from typing import (
    List,
    Optional,
)


class BaseTestFramework(bp.BasePythonPlugin):
    cli_framework: str

    def __init__(
        self,
        project_name: str,
        cli_framework: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        self.file_name = 'cli_test.py'
        super().__init__(project_name, file_renderer, dir_renderer)
        self.cli_framework = cli_framework
        self.name = ''


class Pytest(BaseTestFramework):
    packages = ['pytest', 'pytest-cov']

    def __init__(
        self,
        project_name: str,
        cli_framework: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        super().__init__(project_name, cli_framework, file_renderer, dir_renderer)
        self.name = f'pytest-{self.cli_framework}'
        self.setup_name = 'pytest'
        self.setup_vars = {'cli_framework': cli_framework}
        self.file_location = 'tests'

    def render_file(self):
        if self.cli_framework == 'none':
            self.file_name = 'main_test.py'
            self.main_file = kf.File(f'tests/{self.file_name}')
            self.file_renderer.add_file(self.main_file)
        else:
            super().render_file()


class NoTesting(BaseTestFramework):
    packages: List[str] = []

    def __init__(self, *args):
        pass

    def render_file(self):
        pass

    @property
    def setup_configs(self) -> Optional[str]:
        return None
