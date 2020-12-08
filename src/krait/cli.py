# -*- coding: utf-8 -*-
import click

import krait.utils.plugins as plugin_utils
import krait.lib.plugins.cli_frameworks as kcli
import krait.lib.plugins.test_frameworks as ktest
import krait.lib.plugins.type_checkers as ktype
import krait.lib.plugins.linters as klint
import krait.lib.plugins.automations as kauto
import krait.lib.plugins.help_links as khelp
import krait.lib.renderers as rndr
import krait.main as main

import krait.utils.update as update_utils

from typing import (
    cast,
    Type,
    Dict
)
from pathlib import Path


cli_frameworks = cast(
    Dict[str, Type[kcli.BaseCliFramework]],
    plugin_utils.load_plugins('krait.cli_frameworks')
)
linters = cast(
    Dict[str, Type[klint.BaseLinter]],
    plugin_utils.load_plugins('krait.linters')
)
type_checkers = cast(
    Dict[str, Type[ktype.BaseTypeChecker]],
    plugin_utils.load_plugins('krait.type_checkers')
)
test_frameworks = cast(
    Dict[str, Type[ktest.BaseTestFramework]],
    plugin_utils.load_plugins('krait.test_frameworks')
)
automations = cast(
    Dict[str, Type[kauto.BaseAutomation]],
    plugin_utils.load_plugins('krait.automations')
)

help_link_objects = cast(
    Dict[str, Type[khelp.BaseHelpLinks]],
    plugin_utils.load_plugins('krait.helplinks')
)

help_links = {}

for obj in help_link_objects.values():
    help_links.update(obj.links)

defaults = plugin_utils.get_plugin_defaults()
canonical_name = {
    'lnt': 'Linter',
    'tc': 'Type checker',
    'tf': 'Testing framework',
    'aut': 'Automation system',
    'cli': 'CLI framework',
}


def prompt_if_necessary(ctx, param, val):
    if ctx.params['suppress']:
        return val or defaults[param.name]
    param.default = defaults[param.name]
    param.prompt = canonical_name[param.name]
    return param.prompt_for_value(ctx)


def fail_if_suppress(ctx, param, val):
    if ctx.params['suppress'] and val is None:
        raise click.UsageError(
            f'{param.name} must be specified when using --suppress-interactive'
        )
    if val is None:
        param.prompt = param.name.replace('_', ' ').capitalize()
        return param.prompt_for_value(ctx)
    return val


def setup_prompt(ctx, param, val):
    if ctx.params['suppress'] and val is None:
        raise click.UsageError(
            f'{param.name} must be specified when using --suppress-interactive'
        )
    if val is None:
        if not ctx.params['quiet']:
            click.echo('Setting up new project...')
        return click.prompt('Project name', type=str)

    if not ctx.params['quiet']:
        click.echo(f'Setting up new project {val}...')
    return val


@click.command()
@click.option(
    '-n',
    '--author-name',
    'author_name',
    callback=fail_if_suppress,
    help='Name of the author of the project'
)
@click.option(
    '-e',
    '--email',
    callback=fail_if_suppress,
    help='Email of the author of the project'
)
@click.option(
    '-l',
    '--linter',
    'lnt',
    type=click.Choice(linters.keys(), case_sensitive=False),
    callback=prompt_if_necessary,
    help='Which linter to use with the new project'
)
@click.option(
    '-c',
    '--type-checker',
    'tc',
    type=click.Choice(type_checkers.keys(), case_sensitive=False),
    callback=prompt_if_necessary,
    help='Which type checker to use with the new project'
)
@click.option(
    '-t',
    '--test-framework',
    'tf',
    type=click.Choice(test_frameworks.keys(), case_sensitive=False),
    callback=prompt_if_necessary,
    help='Which test framework to use with the new project'
)
@click.option(
    '-a',
    '--automation',
    'aut',
    type=click.Choice(automations.keys(), case_sensitive=False),
    callback=prompt_if_necessary,
    help='Which automation system to use with the new project'
)
@click.option(
    '--cli',
    type=click.Choice(cli_frameworks.keys(), case_sensitive=False),
    callback=prompt_if_necessary,
    help='Which CLI framework system to use with the new project'
)
@click.option(
    '-s',
    '--suppress-interactive',
    'suppress',
    is_flag=True,
    is_eager=True,
    help='Suppress interactive prompt for missing fields and use defaults instead',
)
@click.option(
    '-q',
    '--quiet',
    is_flag=True,
    is_eager=True,
    help='Suppresses output'
)
@click.argument('project_name', required=False, callback=setup_prompt)
def create(
    author_name: str,
    email: str,
    lnt: str,
    tc: str,
    aut: str,
    tf: str,
    project_name: str,
    cli: str,
    suppress: bool,  # Used in prompting callback, so can't suppress value
    quiet: bool
):
    '''
    Creates a new python project based on the specified options
    '''
    root = Path(f'./{project_name}')
    directories = rndr.DirectoryRenderer(root)
    files = rndr.FileRenderer(root)

    automation = automations[aut](project_name, files, directories, lnt, tc, tf)
    cli_framework = cli_frameworks[cli](project_name, files, directories)
    test_framework = test_frameworks[tf](project_name, cli_framework.name, files, directories)
    linter = linters[lnt](project_name, files, directories)
    type_checker = type_checkers[tc](project_name, files, directories)

    if not quiet:
        directories.set_output(click.echo)
        files.set_output(click.echo)

    main.create(
        project_name=project_name,
        author=author_name,
        email=email,
        cli_framework=cli_framework,
        linter=linter,
        type_checker=type_checker,
        test_framework=test_framework,
        automation=automation,
        directories=directories,
        files=files,
    )


@click.command('set-default')
def set_default():
    pass


@click.command('link')
@click.argument('link', type=click.Choice(help_links.keys()))
def launch_help(link):
    '''
    Launches the specified help site
    '''
    click.launch(help_links[link])


@click.group()
@click.version_option()
@click.option(
    '--no-update',
    is_flag=True,
    help='Prevent checking for updates. '
    'Can be set with env var KRAIT_NO_UPDATE_CHECK'
)
def cli(no_update: bool):  # pragma: no cover
    '''
    Krait is a CLI to help start up new python application. To get
    information on specific subcommands, use `krait [COMMAND] --help`.
    '''
    if not no_update and update_utils.should_check_update():
        update_ver = update_utils.check_for_update()
        if update_ver:
            click.secho(
                'A new version of krait is available!\n'
                f'Install v{update_ver} by running `pip install --upgrade krait`',
                fg='yellow'
            )


# Adding commands to group
cli.add_command(create)  # pragma: no cover
# cli.add_command(set_default)  # pragma: no cover
cli.add_command(launch_help)  # pragma: no cover

if __name__ == '__main__':  # pragma: no cover
    cli()
