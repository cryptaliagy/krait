# -*- coding: utf-8 -*-
'''
Linters to use for Krait
'''

import krait.lib.plugins.base_plugin as bp
import krait.lib.renderers as rndr

from typing import (
    List,
    Dict,
)


class BaseLinter(bp.BasePythonPlugin):
    configurations: Dict[str, str]
    phony_targets = ['lint', 'fmt']


class Flake8(BaseLinter):
    packages = ['flake8']

    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        super().__init__(project_name, file_renderer, dir_renderer)
        self.setup_name = 'flake8'
        self.make_name = 'flake8'


class NoLinter(BaseLinter):
    packages: List[str] = []
