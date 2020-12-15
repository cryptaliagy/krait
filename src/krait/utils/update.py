# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import site
import re

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
        return datetime.fromtimestamp(0)

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
        return subprocess.check_output([
            sys.executable,
            *cmd.split()
        ], stderr=subprocess.DEVNULL).decode('utf-8')
    except subprocess.CalledProcessError:  # Non-zero exit code
        return ''


def run_pip(cmd: str) -> str:
    return run_python_command(f'-m pip {cmd}')


def check_for_update() -> str:
    '''
    Runs a pip search command for the krait package and checks to see
    if the 'LATEST' tag is there. Should only affect packages with version
    smaller than most recently released.
    '''
    try:
        o = run_pip('--timeout 3 --retries 0 search krait')

        pattern = r'LATEST:\s+(\d+\.\d+(\.\d+)?)'
        installed_pattern = r'INSTALLED:\s+(\d+\.\d+(\.\d+)?)'
        m = re.search(pattern, o)
        installed = re.search(installed_pattern, o)
        if m and installed:
            if installed.group(1) == m.group(1):
                return ''
            return m.group(1)
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
        run_pip('install --user --upgrade krait')
    else:
        run_pip('install --upgrade krait')
