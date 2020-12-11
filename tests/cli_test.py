# -*- coding: utf-8 -*-
import pytest
import krait.cli as cli
import unittest.mock as mock

from click.testing import CliRunner
from pathlib import Path


@pytest.fixture()
def mock_configs():
    with mock.patch('krait.cli.config_utils') as mock_config:
        conf = {
            'always_suppress_prompt': False,
            'require_author_name': True,
            'require_author_email': True,
            'auto_check_for_updates': False,
            'always_run_silent': False,
            'aut': 'gha',
            'lnt': 'flake8',
            'tc': 'mypy',
            'prj': 'click',
            'tf': 'pytest',
            'default_author_name': None,
            'default_author_email': None,
            'hours_between_update_checks': 24,
            'config_folder': '',
        }
        mock_config.get_configs.return_value = conf
        config_file = mock.Mock()
        config_file.exists.return_value = True
        mock_config.get_config_file.return_value = config_file
        yield mock_config


@pytest.fixture()
def mock_update():
    with mock.patch('krait.cli.update_utils') as mock_upd:
        mock_upd.should_check_update.return_value = False
        yield mock_upd


@pytest.mark.cli
def test_cli_create(mock_configs, mock_update):
    '''
    Tests that the actual CLI works as expected. As the project
    develops, new tests are likely to be required, such as passing
    in some standard data to make sure it works appropriately.

    For now, this just checks that running the CLI does not produce
    an exception.
    '''

    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        result = runner.invoke(cli.cli, [
            'create',
            '-n',
            'natalia',
            '-e',
            'email',
            'project',
            '-s'
        ])
        project_path = Path(f'{fs}/project')
        assert not result.exception
        assert project_path.exists()
        assert (project_path / 'README.md').exists()
        assert (project_path / 'setup.cfg').exists()
        assert (project_path / 'setup.py').exists()
        assert (project_path / 'src').exists()
        assert (project_path / 'src/project').exists()
        assert (project_path / 'src/project/__init__.py').exists()
        assert (project_path / 'src/project/main.py').exists()
        assert (project_path / 'tests').exists()
        assert (project_path / 'tests/__init__.py').exists()
        assert (project_path / 'tests/cli_test.py').exists()


@pytest.mark.cli
def test_cli_set_default():
    '''
    Tests that the set-default user interactions work appropriately
    '''

    runner = CliRunner()
    result = runner.invoke(cli.set_default)

    assert not result.exception
