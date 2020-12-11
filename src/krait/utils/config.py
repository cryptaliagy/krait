# -*- coding: utf-8 -*-
import click
import json
from pathlib import Path
from typing import (
    Dict,
    Any
)


def get_config_folder() -> Path:
    dir = click.get_app_dir('Krait')
    dir_path = Path(dir)
    if not dir_path.exists():
        dir_path.mkdir()

    return dir_path


def get_config_file() -> Path:
    return get_config_folder() / 'configs.json'


def get_configs() -> Dict[str, Any]:
    configs_file = get_config_file()
    with configs_file.open() as f:
        configs: Dict[str, Any] = json.load(f)

    return configs


def get_config_defaults() -> Dict[str, Any]:
    return {
        'always_suppress_prompt': False,
        'require_author_name': True,
        'require_author_email': True,
        'auto_check_for_updates': True,
        'always_run_silent': False,
        'aut': 'gha',
        'lnt': 'flake8',
        'tc': 'mypy',
        'prj': 'click',
        'tf': 'pytest',
        'default_author_name': None,
        'default_author_email': None,
        'hours_between_update_checks': 24,
    }


def write_configs(config_file: Path, **kwargs: Any):
    if config_file.exists():
        with config_file.open() as f:
            old_configs = json.load(f)
    else:
        old_configs = {}

    old_configs.update(kwargs)

    with config_file.open('w') as f:
        json.dump(old_configs, f)
