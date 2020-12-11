# -*- coding: utf-8 -*-
'''
Allows the `krait` CLI to be run as a python module.
'''
import krait.cli as cli
import sys


if __name__ == '__main__':
    cli.cli.main(prog_name=f'{sys.executable} -m krait')
