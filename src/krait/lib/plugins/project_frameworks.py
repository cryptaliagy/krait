# -*- coding: utf-8 -*-
'''
Cli Frameworks used for Krait
'''

import sys

import krait.lib.plugins.base_plugin as bp
import krait.lib.renderers as rndr
import krait.lib.files as kf
import krait.lib.abc as abc

from typing import (
    List,
)
from pathlib import Path


class BaseProjectFramework(
    bp.BasePythonPlugin,
    abc.AbstractPythonProjectFramework
):
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
        self.project_type = ''
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
        self.project_type = 'cli'


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
        self.project_type = 'lib'


class FlaskProject(BaseProjectFramework):
    packages: List[str] = [
        'flask',
        'gunicorn',
        'python-dotenv'
    ]
    phony_targets: List[str] = [
        'install',
        'build',
        'run',
        'run-d',
        'stop',
    ]

    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        super().__init__(project_name, file_renderer, dir_renderer)

        self.name = 'flask'
        self.file_name = 'app.py'
        self.test_file = 'app_test.py'
        self.project_type = 'web'
        self.rendering_params['project_name'] = project_name
        self.make_name = 'flask'

    def _get_template(self, file_name: str, **kwargs):
        return self.env.get_template(
                f'{self.name}-{file_name}.jinja2'
            ).render(**kwargs)

    def render_file(self):
        super().render_file()

        package_root = f'src/{self.project_name.replace("-","_")}'

        app_config = kf.File(
            f'{package_root}/config.py',
            self._get_template(
                'config.py',
            )
        )

        self.dir_renderer.add_directories(
            Path(f'{package_root}/routes'),
            Path('scripts'),
            Path('docker'),
        )

        init_route = kf.File(
            f'{package_root}/routes/__init__.py',
            self._get_template(
                'routes.py',
                project_name=self.project_name,
            )
        )

        root_route = kf.File(
            f'{package_root}/routes/root.py',
            self._get_template(
                'root.py',
                project_name=self.project_name,
            )
        )

        api_route = kf.File(
            f'{package_root}/routes/api.py',
            self._get_template(
                'api.py',
                project_name=self.project_name,
            )
        )

        env_contents = self._get_template(
            '.env.example',
        )

        env_file = kf.File(
            '.env',
            env_contents,
        )
        env_example_file = kf.File(
            '.env.example',
            env_contents
        )

        run_script = kf.File(
            'scripts/run.sh',
            self._get_template(
                'run.sh',
                project_name=self.project_name,
            ),
            executable=True,
        )

        requirements_file = kf.File(
            'requirements.txt',
            *self.packages
        )

        dockerfile = kf.File(
            'docker/Dockerfile',
            self._get_template(
                'dockerfile',
                version=f'{sys.version_info.major}.{sys.version_info.minor}'
            )
        )

        compose_file = kf.File(
            'docker/docker-compose.yaml',
            self._get_template(
                'docker-compose.yaml',
                project_name=self.project_name,
            )
        )

        self.file_renderer.add_files(
            app_config,
            run_script,
            init_route,
            root_route,
            api_route,
            env_file,
            env_example_file,
            requirements_file,
            dockerfile,
            compose_file
        )
