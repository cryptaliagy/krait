# -*- coding: utf-8 -*-
import krait.lib.abc as abc
import krait.lib.files as kf
import krait.lib.renderers as rndr

from krait.utils.templates import env

from typing import (
    Optional,
    List,
    Dict
)


class BasePythonPlugin(abc.AbstractPythonPlugin):
    packages: List[str]
    file_renderer: rndr.FileRenderer
    dir_renderer: rndr.DirectoryRenderer
    file_name: str
    name: str
    main_file: kf.File
    rendered_file: str
    setup_name: Optional[str]
    setup_vars: Dict[str, str]
    _setup_config: Optional[str]
    file_location: Optional[str]
    rendering_params: Dict[str, str]

    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        super().__init__(project_name, file_renderer, dir_renderer)
        self.rendered_file = ''
        self._setup_config = None
        self.setup_name = None
        self.file_location = None
        self.rendering_params = {}
        self.setup_vars = {}

    def render_file(self):
        if self.file_location:
            self.main_file = kf.File(f'{self.file_location}/{self.file_name}')
        else:
            self.main_file = kf.File(f'src/{self.project_name}/{self.file_name}')
        self.rendered_file = \
            env.get_template(f'{self.name}-{self.file_name}.jinja2').render(**self.rendering_params)
        self.main_file.add_content(self.rendered_file)
        self.main_file.add_content('')  # Newline at end of file
        self.file_renderer.add_file(self.main_file)

    def setup_config(self) -> Optional[str]:
        if self.setup_name is None:
            return None
        if self._setup_config:
            return self._setup_config
        setup_template = env.get_template(f'{self.setup_name}-setup.cfg.jinja2')
        self._setup_config = setup_template.render(**self.setup_vars) + '\n'

        return self._setup_config
