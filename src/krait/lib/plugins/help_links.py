# -*- coding: utf-8 -*-
import krait.lib.abc as abc

from typing import Dict


class BaseHelpLinks(abc.AbstractPlugin):
    links: Dict[str, str]


class KraitHelpLinks(BaseHelpLinks):
    links = {
        'repo': 'https://github.com/taliamax/krait',
        'issues': 'https://github.com/taliamax/krait/issues',
    }
