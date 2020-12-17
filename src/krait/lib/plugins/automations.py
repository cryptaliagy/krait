# -*- coding: utf-8 -*-
'''
Automations used for Krait
'''

import krait.lib.plugins.base_plugin as bp
import krait.lib.renderers as rndr

from typing import Optional
from pathlib import Path


class BaseAutomation(bp.BasePythonPlugin):
    linter: str
    type_checker: str
    test_framework: str

    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer,
        linter: str,
        type_checker: str,
        test_framework: str,
    ):
        super().__init__(project_name, file_renderer, dir_renderer)
        self.rendering_params = {
            'project_name': project_name,
            'linter': linter,
            'type_checker': type_checker,
            'test_framework': test_framework,
        }


class GithubActions(BaseAutomation):
    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer,
        linter: str,
        type_checker: str,
        test_framework: str,
    ):
        super().__init__(
            project_name,
            file_renderer,
            dir_renderer,
            linter,
            type_checker,
            test_framework
        )

        self.file_location = '.github/workflows'
        self.file_name = 'build.yml'
        self.name = 'gha'

        dir_renderer.add_directory(Path('.github'))
        dir_renderer.add_directory(Path('.github/workflows'))


class AzurePipeline(BaseAutomation):
    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer,
        linter: str,
        type_checker: str,
        test_framework: str,
    ):
        super().__init__(
            project_name,
            file_renderer,
            dir_renderer,
            linter,
            type_checker,
            test_framework
        )
        self.file_location = '.'
        self.file_name = 'azure-pipeline.yml'
        self.name = 'azure'


class NoAutomation(BaseAutomation):
    def render_file(self):
        pass

    def setup_config(self) -> Optional[str]:
        return None
