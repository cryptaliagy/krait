# -*- coding: utf-8 -*-
import krait.lib.abc as abc

from typing import (
    Union,
    List,
    Set
)
from pathlib import Path
from krait.utils.templates import env


class File(abc.AbstractFile):
    def __init__(self, path: Union[str, Path], *contents: str):
        self.path = path
        self._contents = list(contents)

    def add_content(self, content: str):
        self._contents.append(content)

    @property
    def contents(self) -> str:
        return '\n'.join(self._contents)


class SetupScript(File):
    def __init__(
        self,
        project_name: str,
        author: str,
        author_email: str,
        cli_framework: abc.AbstractPythonPlugin,
        linter: abc.AbstractPythonPlugin,
        type_checker: abc.AbstractPythonPlugin,
        test_framework: abc.AbstractPythonPlugin,
    ):
        self.path = 'setup.py'
        self.author = author
        self.author_email = author_email
        self.project_name = project_name
        self.cli_framework = cli_framework
        self.linter = linter
        self.type_checker = type_checker
        self.test_framework = test_framework
        self.dependencies: Set[str] = set()
        self.test_dependencies: Set[str] = set()

        if self.cli_framework:
            self.dependencies.update(self.cli_framework.packages)

        if self.linter:
            self.test_dependencies.update(self.linter.packages)

        if self.type_checker:
            self.test_dependencies.update(self.type_checker.packages)

        if self.test_framework:
            self.test_dependencies.update(self.test_framework.packages)

    @property
    def contents(self) -> str:
        setup_template = env.get_template('setup.py.jinja2')
        return setup_template.render(
            project_name=self.project_name,
            author=self.author,
            author_email=self.author_email,
            install_dependencies=[*self.dependencies],
            test_dependencies=[*self.test_dependencies]
        ) + '\n'


class SetupConfig(File):
    plugins: List[abc.AbstractPythonPlugin]

    def __init__(
        self,
        *plugins: abc.AbstractPythonPlugin
    ):
        self.path = 'setup.cfg'
        self.plugins = list(plugins)

    @property
    def contents(self) -> str:
        result = []

        for plugin in self.plugins:
            if plugin.setup_config:
                result.append(plugin.setup_config)

        return '\n'.join(result)
