# -*- coding: utf-8 -*-
'''
Type Checkers used for Krait
'''

import krait.lib.plugins.base_plugin as bp

from typing import List


class BaseTypeChecker(bp.BasePythonPlugin):
    pass


class MyPy(BaseTypeChecker):
    packages = ['mypy']


class NoTypeChecker(BaseTypeChecker):
    packages: List[str] = []
