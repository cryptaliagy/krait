# -*- coding: utf-8 -*-
import jinja2
import krait.utils.config as kconfig

from typing import Optional


class KraitEnv:
    def __init__(self):
        self.env: Optional[jinja2.Environment] = None


def load_path():
    return str(kconfig.get_config_folder() / 'templates')


def get_env():
    if kenv.env is None:
        kenv.env = jinja2.Environment(loader=jinja2.FileSystemLoader(load_path()), autoescape=False)  # noqa
    return kenv.env


kenv = KraitEnv()
