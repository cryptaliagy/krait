# -*- coding: utf-8 -*-
from typing import (
    Union,
    List,
    Set,
    Optional,
)
from pathlib import Path

import krait.lib.abc as abc
from krait.utils.templates import get_env


class File(abc.AbstractFile):
    def __init__(
        self,
        path: Union[str, Path],
        *contents: str,
        executable: bool = False
    ):
        self.path = path
        self._contents = list(contents)
        self.executable = executable

    def add_content(self, content: str):
        self._contents.append(content)

    @property
    def contents(self) -> str:
        return '\n'.join(self._contents)


class SetupScript(File):
    def __init__(
        self,
        project_name: str,
        author: Optional[str],
        author_email: Optional[str],
        project_framework: abc.AbstractPythonProjectFramework,
        linter: abc.AbstractPythonPlugin,
        type_checker: abc.AbstractPythonPlugin,
        test_framework: abc.AbstractPythonPlugin,
    ):
        super().__init__('setup.py')
        self.author = author or ''
        self.author_email = author_email or ''
        self.project_name = project_name
        self.project_framework = project_framework
        self.linter = linter
        self.type_checker = type_checker
        self.test_framework = test_framework
        self.dependencies: Set[str] = set()
        self.test_dependencies: Set[str] = set()

        if self.project_framework:
            self.dependencies.update(self.project_framework.packages)

        if self.linter:
            self.test_dependencies.update(self.linter.packages)

        if self.type_checker:
            self.test_dependencies.update(self.type_checker.packages)

        if self.test_framework:
            self.test_dependencies.update(self.test_framework.packages)

    @property
    def contents(self) -> str:
        setup_template = get_env().get_template('setup.py.jinja2')
        return setup_template.render(
            project_name=self.project_name,
            author=self.author,
            author_email=self.author_email,
            install_dependencies=[*self.dependencies],
            test_dependencies=[*self.test_dependencies],
            project_type=self.project_framework.project_type,
        ) + '\n'


class SetupConfig(File):
    plugins: List[abc.AbstractPythonPlugin]

    def __init__(
        self,
        *plugins: abc.AbstractPythonPlugin
    ):
        super().__init__('setup.cfg')
        self.plugins = list(plugins)

    @property
    def contents(self) -> str:
        result = []

        for plugin in self.plugins:
            config = plugin.setup_config()
            if config:
                result.append(config)

        return '\n'.join(result)


class MakeFile(File):
    plugins: List[abc.AbstractPlugin]

    def __init__(
        self,
        *plugins: abc.AbstractPlugin
    ):
        super().__init__('Makefile')
        self.plugins = list(plugins)

    @property
    def contents(self) -> str:
        result = []

        result.append(
            get_env().get_template('base-makefile.jinja2').render()
        )

        for plugin in self.plugins:
            targets = plugin.make_targets()
            if targets:
                result.append(targets)

        return '\n\n'.join(result)
