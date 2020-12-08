# -*- coding: utf-8 -*-
'''
Linters to use for Krait
'''

import krait.lib.plugins.base_plugin as bp

from typing import (
    List,
    Dict,
)


class BaseLinter(bp.BasePythonPlugin):
    configurations: Dict[str, str]


class Flake8(BaseLinter):
    packages = ['flake8']


class NoLinter(BaseLinter):
    packages: List[str] = []
