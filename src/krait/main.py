# -*- coding: utf-8 -*-
import click
import logging
import pathlib

import krait.utils.plugins as plugin_utils
import krait.lib.abc as abc
import krait.lib.renderers as rndr

from typing import (
    cast,
    Type,
)


logging.basicConfig(level=logging.INFO)


cli_frameworks = plugin_utils.load_plugins('krait.cli_frameworks')
linters = plugin_utils.load_plugins('krait.linters')
type_checkers = plugin_utils.load_plugins('krait.type_checkers')
test_frameworks = plugin_utils.load_plugins('krait.test_frameworks')
automations = plugin_utils.load_plugins('krait.automations')


@click.command()
@click.option('-n', '--name', help='Name of the author of the project')
@click.option('-e', '--email', help='Email of the author of the project')
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
@click.option(
    '--cli',
    type=click.Choice([*cli_frameworks.keys()], case_sensitive=False),
    default='click',
    help='Which CLI framework system to use with the new project'
)
@click.argument('project_name', required=False)
def create(
    name: str,
    email: str,
    linter: str,
    type_checker: str,
    automation: str,
    test_framework: str,
    project_name: str,
    cli: str,
):
    '''
    Create a new python project with the specified options
    '''
    directories = rndr.DirectoryRenderer(
        pathlib.Path(project_name),
        *map(
            lambda p: pathlib.Path(p),
            [
                'src',
                f'src/{project_name}',
                'tests'
            ]
        ))

    files = rndr.FileRenderer(directories.root, *map(
        lambda p: rndr.File(p),
        [
            'setup.cfg',
            f'src/{project_name}/__init__.py',
            'tests/__init__.py'
        ]
    ))

    cli_framework_class = cast(  # Cast to appropriate class type
        Type[abc.AbstractCliFramework],
        cli_frameworks.get(cli, None)
    )

    cli_framework = cli_framework_class(project_name, files, directories)
    cli_framework.render_file()

    readme_file = rndr.File('README.md', f'# {project_name}')
    setup_script = rndr.SetupScript(project_name, name, email, cli_framework, None, None, None)

    files.add_file(readme_file)
    files.add_file(setup_script)
    directories.create_all()
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
