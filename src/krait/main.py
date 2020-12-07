# -*- coding: utf-8 -*-
import click
import logging
import pathlib
import os

import krait.utils.plugins as plugin_utils
import krait.lib.renderers as rndr


logging.basicConfig(level=logging.INFO)


linters = plugin_utils.load_plugins('krait.linters')
type_checkers = plugin_utils.load_plugins('krait.type_checkers')
test_frameworks = plugin_utils.load_plugins('krait.test_frameworks')
automations = plugin_utils.load_plugins('krait.automations')


@click.command()
@click.option(
    '-l',
    '--linter',
    type=click.Choice([*linters.keys(), 'none'], case_sensitive=False),
    help='Which linter to use with the new project'
)
@click.option(
    '-c',
    '--type-checker',
    'type_checker',
    type=click.Choice([*type_checkers.keys(), 'none'], case_sensitive=False),
    help='Which type checker to use with the new project'
)
@click.option(
    '-t',
    '--test-framework',
    'test_framework',
    type=click.Choice([*test_frameworks.keys(), 'none'], case_sensitive=False),
    help='Which test framework to use with the new project'
)
@click.option(
    '-a',
    '--automation',
    type=click.Choice([*automations.keys(), 'none'], case_sensitive=False),
    help='Which automation system to use with the new project'
)
@click.argument('project_name', required=False)
def create(
    linter: str,
    type_checker: str,
    automation: str,
    test_framework: str,
    project_name: str
):
    '''
    Create a new python project with the specified options
    '''
    directories = rndr.DirectoryRenderer(*map(
        lambda p: pathlib.Path(p),
        [
            f'{project_name}',
            f'{project_name}/src',
            f'{project_name}/src/{project_name}',
            f'{project_name}/tests'
        ]
    ))

    directories.create_all()

    os.chdir(f'./{project_name}')

    files = rndr.FileRenderer(*map(
        lambda p: rndr.File(p),
        [
            'setup.py',
            'setup.cfg',
            'README.md',
            f'src/{project_name}/__init__.py',
            'tests/__init__.py'
        ]
    ))

    files.write_all()


@click.command('set-default')
def set_default():
    '''
    Set default options to use in `krait create`. These will be stored in
    a global config file.
    '''
    pass


@click.command('help')
def launch_help():
    '''
    Launches the specified help site
    '''


@click.group()
@click.version_option()
def main():  # pragma: no cover
    pass


# Adding commands to group
main.add_command(create)  # pragma: no cover
main.add_command(set_default)  # pragma: no cover
main.add_command(launch_help)  # pragma: no cover

if __name__ == '__main__':  # pragma: no cover
    main()
