# -*- coding: utf-8 -*-
'''
Cli Frameworks used for Krait
'''

import krait.lib.abc as abc
import krait.lib.renderers as rndr
from krait.utils.templates import env


class ClickFramework(abc.AbstractCliFramework):
    packages = ['click']

    def __init__(
        self,
        project_name: str,
        file_renderer: rndr.FileRenderer,
        dir_renderer: rndr.DirectoryRenderer
    ):
        self.rendered_file = ''
        self.main_file = rndr.File(f'src/{project_name}/main.py')
        self.file_renderer: rndr.FileRenderer = file_renderer
        self.dir_renderer: rndr.DirectoryRenderer = dir_renderer

    def render_file(self):
        '''
        Render the main.py file and inserts it into the file renderer
        '''
        self.rendered_file = env.get_template('click-main.py.jinja2').render()
        self.main_file.add_content(self.rendered_file)
        self.main_file.add_content('')  # Newline at end of file
        self.file_renderer.add_file(self.main_file)
