# -*- coding: utf-8 -*-
'''
Automations used for Krait
'''

import krait.lib.plugins.base_plugin as bp


class BaseAutomation(bp.BasePythonPlugin):
    linter: str
    type_checker: str
    test_framework: str


class GithubActions(BaseAutomation):
    pass


class NoAutomation(BaseAutomation):
    pass
