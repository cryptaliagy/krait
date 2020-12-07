# -*- coding: utf-8 -*-
'''
Linters to use for Krait
'''

import krait.lib.abc as abc


class Flake8(abc.AbstractLinter):
    packages = ['flake8']
