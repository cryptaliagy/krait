# -*- coding: utf-8 -*-
'''
Cli Frameworks used for Krait
'''

import krait.lib.plugins.base_plugin as bp
import krait.lib.renderers as rndr
import krait.lib.files as kf

from typing import (
    List,
)
from pathlib import Path


class BaseProjectFramework(bp.BasePythonPlugin):
    file_renderer: rndr.FileRenderer
    dir_renderer: rndr.DirectoryRenderer
    test_file: str
    name: str

    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        self.file_name = 'main.py'
        self.test_file = ''
        package_dir = Path(f'src/{project_name.replace("-", "_")}')
        module_init = kf.File(
            package_dir / '__init__.py'
        )
        dir_renderer.add_directories(
            Path('src'),
            package_dir
        )
        file_renderer.add_file(module_init)
        super().__init__(project_name, file_renderer, dir_renderer)


class ClickFramework(BaseProjectFramework):
    packages = ['click']

    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        super().__init__(project_name, file_renderer, dir_renderer)
        self.name = 'click'
        self.test_file = 'cli_test.py'


class LibraryProject(BaseProjectFramework):
    packages: List[str] = []

    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        super().__init__(project_name, file_renderer, dir_renderer)
        self.name = 'library'
        self.file_name = 'lib.py'
        self.test_file = 'lib_test.py'
