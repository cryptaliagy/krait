# -*- coding: utf-8 -*-
import click


@click.command()
def main():
    '''
    Ideally this function should be restricted to the logic
    required to run the CLI. Any logic that would be
    used to actually run the application should be extracted into
    different functions, possibly in different files. Creating a lib.py
    could be helpful for this case, or making more packages as appropriate.

    Reducing how much code is actually added to this function will let the
    testing of the CLI portion of the application be substantially easier to
    write and understand.
    '''
    pass


if __name__ == '__main__':  # pragma: no cover
    main()
