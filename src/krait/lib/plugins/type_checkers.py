# -*- coding: utf-8 -*-
'''
Type Checkers used for Krait
'''

import krait.lib.plugins.base_plugin as bp
import krait.lib.renderers as rndr

from typing import List


class BaseTypeChecker(bp.BasePythonPlugin):
    pass


class MyPy(BaseTypeChecker):
    packages = ['mypy']

    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        super().__init__(project_name, file_renderer, dir_renderer)
        self.setup_name = 'mypy'


class NoTypeChecker(BaseTypeChecker):
    packages: List[str] = []
