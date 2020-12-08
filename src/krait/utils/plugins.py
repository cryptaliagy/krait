# -*- coding: utf-8 -*-
'''
Plugin related functions
'''

import pkg_resources
import logging

import krait.lib.abc as abc

from typing import (
    Dict,
)


def load_plugins(plugin_type: str) -> Dict[str, abc.AbstractPlugin]:
    plugins: Dict[str, abc.AbstractPlugin] = {}

    for entry_point in pkg_resources.iter_entry_points(plugin_type):
        logging.debug('Found entry point for %s', entry_point.name)
        try:
            entry_point.require()
            plugins[entry_point.name] = entry_point.load()
        except pkg_resources.DistributionNotFound as e:  # pragma: no cover
            logging.debug(
                'Received error when trying to load %s: %s',
                entry_point.name,
                e
            )

    return plugins


def get_plugin_defaults() -> Dict[str, str]:
    defaults = {
        'aut': 'gha',
        'lnt': 'flake8',
        'tc': 'mypy',
        'cli': 'click',
        'tf': 'pytest',
    }

    return defaults
