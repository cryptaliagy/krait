# -*- coding: utf-8 -*-
'''
Cli Frameworks used for Krait
'''

import krait.lib.plugins.base_plugin as bp
import krait.lib.renderers as rndr

from typing import (
    List,
    Optional,
)


class BaseCliFramework(bp.BasePythonPlugin):
    file_renderer: rndr.FileRenderer
    dir_renderer: rndr.DirectoryRenderer
    name: str

    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        self.file_name = 'main.py'
        super().__init__(project_name, file_renderer, dir_renderer)

    @property
    def setup_configs(self) -> Optional[str]:
        return None


class ClickFramework(BaseCliFramework):
    packages = ['click']

    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        super().__init__(project_name, file_renderer, dir_renderer)
        self.name = 'click'

    @property
    def setup_configs(self) -> Optional[str]:
        return None


class NoCliFramework(BaseCliFramework):
    packages: List[str] = []

    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        super().__init__(project_name, file_renderer, dir_renderer)
        self.name = 'none'
