# -*- coding: utf-8 -*-
'''
Abstract base classes for Krait
'''

from typing import (
    Dict,
    List,
)


class AbstractPlugin:
    project_name: str


class AbstractVCS(AbstractPlugin):
    pass


class AbstractPythonPlugin(AbstractPlugin):
    packages: List[str]


class AbstractLinter(AbstractPythonPlugin):
    configurations: Dict[str, str]


class AbstractTypeChecker(AbstractPythonPlugin):
    pass


class AbstractTestFramework(AbstractPythonPlugin):
    pass


class AbstractAutomation(AbstractPythonPlugin):
    linter: str
    type_checker: str
    test_framework: str
