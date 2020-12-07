# -*- coding: utf-8 -*-
import pytest
import krait.main as main

from click.testing import CliRunner
from pathlib import Path


@pytest.mark.cli
def test_cli_create():
    '''
    Tests that the actual CLI works as expected. As the project
    develops, new tests are likely to be required, such as passing
    in some standard data to make sure it works appropriately.

    For now, this just checks that running the CLI does not produce
    an exception.
    '''

    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        result = runner.invoke(main.create, ['project'])
        project_path = Path(f'{fs}/project')
        assert not result.exception
        assert project_path.exists()
        assert (project_path / 'README.md').exists()
        assert (project_path / 'setup.cfg').exists()
        assert (project_path / 'setup.py').exists()
        assert (project_path / 'src').exists()
        assert (project_path / 'src/project').exists()
        assert (project_path / 'src/project/__init__.py').exists()
        assert (project_path / 'tests').exists()
        assert (project_path / 'tests/__init__.py').exists()


@pytest.mark.cli
def test_cli_set_default():
    '''
    Tests that the set-default user interactions work appropriately
    '''

    runner = CliRunner()
    result = runner.invoke(main.set_default)

    assert not result.exception
