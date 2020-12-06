# -*- coding: utf-8 -*-
import click


@click.command()
def create():
    '''
    Create a new python project with the specified options
    '''
    pass


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
