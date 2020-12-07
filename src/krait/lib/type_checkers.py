# -*- coding: utf-8 -*-
'''
Type Checkers used for Krait
'''

import krait.lib.abc as abc


class MyPy(abc.AbstractTypeChecker):
    packages = ['mypy']
