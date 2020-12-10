# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import click
import site
import re


def should_check_update(ctx: click.Context) -> bool:
    check_update = os.environ.get('KRAIT_NO_UPDATE_CHECK', None) is None
    is_updating = ctx.invoked_subcommand == 'update'
    return check_update and not is_updating


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
        subprocess.call([
            sys.executable,
            *'-m pip install --user --upgrade krait'.split()
        ])
    else:
        subprocess.call([
            sys.executable,
            *'-m pip install --upgrade krait'.split()
        ])
