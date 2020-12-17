# -*- coding: utf-8 -*-

from typing import (
    cast,
    Type,
    Dict,
    List,
    Union,
    Optional,
)
from pathlib import Path

import click
import pydeepmerge as pdm  # type: ignore
import krait.utils.plugins as plugin_utils
import krait.utils.config as config_utils
import krait.lib.plugins.project_frameworks as kproj
import krait.lib.plugins.test_frameworks as ktest
import krait.lib.plugins.type_checkers as ktype
import krait.lib.plugins.linters as klint
import krait.lib.plugins.automations as kauto
import krait.lib.plugins.help_links as khelp
import krait.lib.plugins.vcs as kvcs
import krait.lib.renderers as rndr
import krait.main as main

import krait.utils.update as update_utils


project_frameworks = cast(
    Dict[str, Type[kproj.BaseProjectFramework]],
    plugin_utils.load_plugins('krait.project_frameworks')
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
vcs_types = cast(
    Dict[str, Type[kvcs.BaseVCSPlugin]],
    plugin_utils.load_plugins('krait.vcs')
)

help_link_objects = cast(
    Dict[str, Type[khelp.BaseHelpLinks]],
    plugin_utils.load_plugins('krait.helplinks')
)

help_links = {}

for obj in help_link_objects.values():
    help_links.update(obj.links)


canonical_name = {
    'lnt': 'Linter',
    'tc': 'Type checker',
    'tf': 'Testing framework',
    'aut': 'Automation system',
    'prj': 'Project framework',
    'vcs_type': 'VCS System',
    'always_suppress_prompt': 'Always suppress interactive prompt?',
    'require_author_name': 'Require projects to have an author name?',
    'require_author_email': 'Require projects to have an author email?',
    'auto_check_for_updates': 'Check for new versions of krait?',
    'always_run_silent': 'Display file creation outputs?',
}


def prompt_if_necessary(ctx, param, val):
    if ctx.obj['suppress']:
        return val or ctx.obj[param.name]
    param.default = ctx.obj[param.name]
    param.prompt = canonical_name[param.name]
    return param.prompt_for_value(ctx)


def fail_if_suppress(ctx, param, val):
    if ctx.obj['suppress'] and val is None and ctx.obj[f'require_{param.name}']:
        raise click.UsageError(
            f'{param.name} must be specified when using --suppress-interactive'
        )
    if val is None and ctx.obj[f'require_{param.name}']:
        param.prompt = param.name.replace('_', ' ').capitalize()
        return param.prompt_for_value(ctx)
    return val


def setup_prompt(ctx, param, val):
    if ctx.obj['suppress'] and val is None:
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


def setup_suppress(ctx, param, val):
    ctx.obj['suppress'] = val or ctx.obj['always_suppress_prompt']
    return val


def setup_quiet(ctx, param, val):
    return val or ctx.obj['always_run_silent']


def default_value_prompt(val_name: str, choices: List[str]):
    return click.prompt(
        f'Which {val_name} would you like as default?',
        type=click.Choice(choices, case_sensitive=False)
    )


def yes_no_prompt(msg: str, default: bool = True):
    return click.prompt(
        msg,
        type=click.Choice(['yes', 'no'], case_sensitive=False),
        default='yes' if default else 'no'
    ) == 'yes'


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
    'author_email',
    callback=fail_if_suppress,
    help='Email of the author of the project'
)
@click.option(
    '-l',
    '--linter',
    'lnt',
    type=click.Choice(plugin_utils.get_plugin_keys(linters), case_sensitive=False),
    callback=prompt_if_necessary,
    help='Which linter to use with the new project'
)
@click.option(
    '-c',
    '--type-checker',
    'tc',
    type=click.Choice(plugin_utils.get_plugin_keys(type_checkers), case_sensitive=False),
    callback=prompt_if_necessary,
    help='Which type checker to use with the new project'
)
@click.option(
    '-t',
    '--test-framework',
    'tf',
    type=click.Choice(plugin_utils.get_plugin_keys(test_frameworks), case_sensitive=False),
    callback=prompt_if_necessary,
    help='Which test framework to use with the new project'
)
@click.option(
    '-a',
    '--automation',
    'aut',
    type=click.Choice(plugin_utils.get_plugin_keys(automations), case_sensitive=False),
    callback=prompt_if_necessary,
    help='Which automation system to use with the new project'
)
@click.option(
    '-p',
    '--project-type',
    'prj',
    type=click.Choice(plugin_utils.get_plugin_keys(project_frameworks), case_sensitive=False),
    callback=prompt_if_necessary,
    help='Which project framework to use with the new project'
)
@click.option(
    '--suppress-interactive/--no-suppress-interactive',
    '-s',
    'suppress',
    default=False,
    is_eager=True,
    expose_value=False,
    callback=setup_suppress,
    help='Suppress interactive prompt for missing fields and use defaults instead',
)
@click.option(
    '--quiet/--no-quiet',
    '-q',
    'quiet',
    default=False,
    is_eager=True,
    callback=setup_quiet,
    help='Suppresses output'
)
@click.option(
    '--vcs',
    'vcs_type',
    type=click.Choice(plugin_utils.get_plugin_keys(vcs_types), case_sensitive=False),
    callback=prompt_if_necessary,
    help='What VCS system to use with the new project'
)
@click.argument('project_name', required=False, callback=setup_prompt)
def create(
    author_name: str,
    author_email: str,
    lnt: str,
    tc: str,
    aut: str,
    tf: str,
    project_name: str,
    prj: str,
    quiet: bool,
    vcs_type: str,
):
    '''
    Creates a new python project based on the specified options
    '''
    root = Path(f'./{project_name}')
    directories = rndr.DirectoryRenderer(root)
    files = rndr.FileRenderer(root)

    automation = automations[aut](project_name, files, directories, lnt, tc, tf)
    project_framework = project_frameworks[prj](project_name, files, directories)
    test_framework = test_frameworks[tf](project_name, project_framework, files, directories)
    linter = linters[lnt](project_name, files, directories)
    type_checker = type_checkers[tc](project_name, files, directories)
    vcs = vcs_types[vcs_type](project_name, files, directories)

    directories.attach_vcs(vcs)

    if not quiet:
        directories.set_output(click.echo)
        files.set_output(click.echo)

    main.create(
        project_name=project_name,
        author=author_name,
        email=author_email,
        project_framework=project_framework,
        linter=linter,
        type_checker=type_checker,
        test_framework=test_framework,
        automation=automation,
        directories=directories,
        files=files,
    )


@click.command('set-config')
@click.option(
    '--require-author-name',
    'require_author_name',
    type=click.Choice(['yes', 'no'], case_sensitive=False),
    help='Whether or not to require author name for new projects'
)
@click.option(
    '--require-author-email',
    'require_author_email',
    type=click.Choice(['yes', 'no'], case_sensitive=False),
    help='Email of the author of the project'
)
@click.option(
    '-l',
    '--linter',
    'lnt',
    type=click.Choice(plugin_utils.get_plugin_keys(linters), case_sensitive=False),
    help='Which linter to use with new projects'
)
@click.option(
    '-c',
    '--type-checker',
    'tc',
    type=click.Choice(plugin_utils.get_plugin_keys(type_checkers), case_sensitive=False),
    help='Which type checker to use with new projects'
)
@click.option(
    '-t',
    '--test-framework',
    'tf',
    type=click.Choice(plugin_utils.get_plugin_keys(test_frameworks), case_sensitive=False),
    help='Which test framework to use with new projects'
)
@click.option(
    '-a',
    '--automation',
    'aut',
    type=click.Choice(plugin_utils.get_plugin_keys(automations), case_sensitive=False),
    help='Which automation system to use with new projects'
)
@click.option(
    '-p',
    '--project-type',
    'prj',
    type=click.Choice(plugin_utils.get_plugin_keys(project_frameworks), case_sensitive=False),
    help='Which project framework to use with new projects'
)
@click.option(
    '--vcs',
    'vcs_type',
    type=click.Choice(plugin_utils.get_plugin_keys(vcs_types), case_sensitive=False),
    help='What VCS system to use with the new project'
)
@click.option(
    '--always-suppress-prompt',
    'always_suppress_prompt',
    type=click.Choice(['yes', 'no'], case_sensitive=False),
    help='Suppress interactive prompt for missing fields and use defaults instead',
)
@click.option(
    '--always-run-silent',
    'always_run_silent',
    type=click.Choice(['yes', 'no'], case_sensitive=False),
    help='Suppresses output from krait on all projects'
)
@click.option(
    '--check-for-updates',
    'auto_check_for_updates',
    type=click.Choice(['yes', 'no'], case_sensitive=False),
    help='Whether Krait should automatically check for updates when run'
)
@click.option(
    '--set-update-cooldown',
    'hours_between_update_checks',
    type=int,
    help='The number of hours Krait will wait between checking for updates'
)
def set_default(**kwargs: Optional[str]):
    '''
    Sets the specified configurations as the new defaults
    '''
    configs = {}
    for key in kwargs:
        val: Union[bool, str, None] = kwargs[key]
        if val is None:
            continue
        if val in ['yes', 'no']:
            val = cast(bool, val == 'yes')
        configs[key] = val
    config_file = config_utils.get_config_file()
    config_utils.write_configs(config_file, **configs)


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
    'Can be set with env var KRAIT_NO_UPDATE_CHECK',
)
@click.option(
    '--skip-config',
    is_flag=True,
    help='Set up krait with defaults if not yet configured'
)
@click.pass_context
def cli(
    ctx: click.Context,
    no_update: bool,
    skip_config: bool,
):  # pragma: no cover
    '''
    Krait is a CLI to help start up new python application. To get
    information on specific subcommands, use `krait [COMMAND] --help`.
    '''
    config_file = config_utils.get_config_file()

    if not config_file.exists():
        click.secho('Welcome to Krait!', fg='green')
        click.echo(
            'Krait is starting up for the first time '
            'and requires configuration'
        )
        if skip_config:
            use_defaults = True
        else:
            use_defaults = yes_no_prompt(
                'Would you like to use the default configurations?\n'
                'Note: this can be changed later with `krait set-default`'
            )
        if use_defaults:
            configs = config_utils.get_config_defaults()
        else:
            configs = {
                'lnt': default_value_prompt(
                    'linter',
                    plugin_utils.get_plugin_keys(linters)
                ),
                'tc': default_value_prompt(
                    'type checker',
                    plugin_utils.get_plugin_keys(type_checkers)
                ),
                'tf': default_value_prompt(
                    'testing framework',
                    plugin_utils.get_plugin_keys(test_frameworks)
                ),
                'aut': default_value_prompt(
                    'automation system',
                    plugin_utils.get_plugin_keys(automations)
                ),
                'prj': default_value_prompt(
                    'project framework',
                    plugin_utils.get_plugin_keys(project_frameworks)
                ),
                'vcs_type': default_value_prompt(
                    'VCS Type',
                    plugin_utils.get_plugin_keys(vcs_types)
                ),
                'always_suppress_prompt': yes_no_prompt(
                    'Always suppress interactive prompt?',
                    default=False
                ),
                'require_author_name': yes_no_prompt(
                    'Require projects to have an author name?'
                ),
                'require_author_email': yes_no_prompt(
                    'Require projects to have an author email?'
                ),
                'auto_check_for_updates': yes_no_prompt(
                    'Check for new versions of krait?'
                ),
                'always_run_silent': yes_no_prompt(
                    'Display file creation outputs?'
                ),
            }

        config_utils.write_configs(
            config_file,
            **configs
        )
    else:
        configs = config_utils.get_configs()
        defaults = config_utils.get_config_defaults()
        # Ensure new config options are loaded
        updated_configs = pdm.deep_merge(defaults, configs)
        if updated_configs != configs:
            config_utils.write_configs(
                config_file,
                **configs
            )
        configs = updated_configs

    configs['config_folder'] = config_file.parent

    ctx.obj = configs
    if not no_update and update_utils.should_check_update(ctx):
        update_ver = update_utils.check_for_update()
        if update_ver:
            click.secho(
                'A new version of krait is available!\n'
                f'Install v{update_ver} by running `krait update`',
                fg='yellow'
            )


@click.command('show-config')
@click.pass_obj
def show_config(obj):
    '''
    Displays the current configurations
    '''
    click.secho('Displaying current Krait configurations', fg='green')
    for key in obj:
        if obj[key] is not None:
            if obj[key] is True:
                fg = 'green'
            elif obj[key] is False:
                fg = 'red'
            else:
                fg = 'cyan'
            if len(key) < 5:
                name = canonical_name[key]
            else:
                name = key

            click.secho(f'{name.capitalize().replace("_", " ")}: ', nl=False, fg='magenta')
            click.secho(f'{obj[key]}', fg=fg)


@click.command('upgrade')
def update():
    '''
    Runs the pip upgrade process.

    This checks if `krait` was installed globally or with --user
    '''
    update_utils.run_update()


# Adding commands to group
cli.add_command(create)  # pragma: no cover
cli.add_command(set_default)  # pragma: no cover
cli.add_command(show_config)  # pragma: no cover
cli.add_command(launch_help)  # pragma: no cover
cli.add_command(update)  # pragma: no cover

if __name__ == '__main__':  # pragma: no cover
    cli()
