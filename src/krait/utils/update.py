# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import site
import json

from urllib import request
from datetime import datetime
from pathlib import Path

import click


def get_update_file(ctx: click.Context) -> Path:
    configs_folder = ctx.obj['config_folder']
    update_time_file = configs_folder / 'last_update'
    update_time_file.touch()  # Create the file if it doesn't exist

    return update_time_file


def get_last_update_time(ctx: click.Context) -> datetime:
    update_file = get_update_file(ctx)
    with update_file.open() as f:
        data = f.read()

    if data == '':  # File is empty
        return datetime.min

    return datetime.fromtimestamp(float(data))


def set_last_update_to_now(ctx: click.Context):
    update_file = get_update_file(ctx)

    with update_file.open('w') as f:
        f.write(str(datetime.now().timestamp()))


def should_check_update(ctx: click.Context) -> bool:
    '''
    Checks that the command was not executed with --help,
    that the KRAIT_NO_UPDATE_CHECK variable was not passed,
    that auto_check_for_updates is enabled in the configs,
    that the CLI is not currently executing the 'krait update' command,
    and that the minimum defined hours have passed since the last update
    has been executed. If it is determined that an update should be checked,
    this function also sets the last update time to the current one.
    '''
    UPDATE_COOLDOWN = 60 * 60 * ctx.obj['hours_between_update_checks']
    executing_help = '--help' in sys.argv
    check_update = os.environ.get('KRAIT_NO_UPDATE_CHECK', None) is None
    default_config_enabled = ctx.obj['auto_check_for_updates']
    is_updating = ctx.invoked_subcommand == 'update'
    update_time = get_last_update_time(ctx)
    time_difference = datetime.now() - update_time
    run_update_check = (
        not executing_help and
        check_update and
        default_config_enabled and
        not is_updating and
        time_difference.total_seconds() > UPDATE_COOLDOWN
    )

    if run_update_check:
        set_last_update_to_now(ctx)

    return run_update_check


def run_python_command(cmd: str) -> str:
    try:
        o = subprocess.check_output([
            sys.executable,
            *cmd.split()
        ], stderr=subprocess.DEVNULL).decode('utf-8')
    except Exception:
        o = ''

    return o


def run_pip(cmd: str) -> str:
    return run_python_command(f'-m pip {cmd}')


def check_for_update() -> str:
    '''
    Queries the Github releases API to get the latest Krait release.

    If a newer release exists, return the version. Otherwise, return
    the empty string
    '''
    try:
        api_data = request.urlopen(
            'https://api.github.com/repos/taliamax/krait/releases/latest'
        ).read()

        json_data = json.loads(api_data)
        tag_version = json_data['tag_name']
        o = run_pip('show krait | grep Version')

        if tag_version in o:
            return ''
        return tag_version

    except Exception:
        pass
    return ''


def run_update():
    '''
    Checks if `krait` is installed with --user and runs the appropriate
    pip command.

    The install command is run through subprocess.call instead of
    run_pip since it makes sense to pipe that output directly to
    stdout and stderr.
    '''
    o = run_pip('show krait')
    if site.USER_SITE is not None and site.USER_SITE in o:
        subprocess.call([
            sys.executable,
            *'-m pip install --user --upgrade krait'.split()
        ])
    else:
        subprocess.call([
            sys.executable,
            *'-m pip install --upgrade krait'.split()
        ])
