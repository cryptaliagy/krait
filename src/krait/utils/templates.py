# -*- coding: utf-8 -*-
import jinja2
import krait.utils.config as kconfig


env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(kconfig.get_config_folder() / 'templates')), autoescape=False)  # noqa
