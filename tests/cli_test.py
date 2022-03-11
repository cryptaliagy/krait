# -*- coding: utf-8 -*-
import pytest
import krait.cli as cli
import unittest.mock as mock
import pkg_resources

from click.testing import CliRunner
from pathlib import Path

from typing import (
    Dict,
    List,
)


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
            'vcs_type': 'none',
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
def mock_templates():
    with mock.patch('krait.utils.templates.kconfig') as mock_config:
        file_path = Path(pkg_resources.resource_filename(__name__, ''))
        mock_config.get_config_folder.return_value = file_path.parent / 'src/krait'
        yield mock_config


@pytest.fixture()
def mock_update():
    with mock.patch('krait.cli.update_utils') as mock_upd:
        mock_upd.should_check_update.return_value = False
        yield mock_upd


common_files: List[str] = [
    'README.md',
    'setup.cfg',
    'setup.py',
    'MANIFEST.in',
    'Makefile',
]

expected_files_for_config: Dict[str, List[str]] = {
    '-a gha -l flake8 -c mypy -p click -t pytest': [
        'src/project/__init__.py',
        'src/project/main.py',
        'tests/__init__.py',
        'tests/cli_test.py',
        '.github/workflows/build.yml',
    ],
    '-a none -l none -c none -p click -t pytest': [
        'src/project/__init__.py',
        'src/project/main.py',
        'tests/__init__.py',
        'tests/cli_test.py',
        '!.github/workflows/build.yml',
    ],
    '-a none -l none -c none -p library -t pytest': [
        'src/project/__init__.py',
        'src/project/lib.py',
        'tests/__init__.py',
        'tests/lib_test.py',
        '!.github/workflows/build.yml',
    ],
    '-a gha -p library -t pytest': [
        'src/project/__init__.py',
        'src/project/lib.py',
        'tests/__init__.py',
        'tests/lib_test.py',
        '!tests/cli_test.py',
        '.github/workflows/build.yml',
    ],
    '-a none -p library -t none': [
        'src/project/__init__.py',
        'src/project/lib.py',
        '!tests/__init__.py',
        '!tests/lib_test.py',
        '!tests/cli_test.py',
        '!.github/workflows/build.yml',
    ],
    '-a none -p flask -t none -l none -c none': [
        'src/project/__init__.py',
        'src/project/app.py',
        'src/project/config.py',
        'src/project/routes/__init__.py',
        'src/project/routes/root.py',
        'src/project/routes/api.py',
        'docker/Dockerfile',
        'docker/docker-compose.yaml',
        '!tests/__init__.py',
        '!tests/app_test.py',
        '!.github/workflows/build.yml',
    ],
    '-a gha -p flask -t none -l none -c none': [
        'src/project/__init__.py',
        'src/project/app.py',
        'src/project/config.py',
        'src/project/routes/__init__.py',
        'src/project/routes/root.py',
        'src/project/routes/api.py',
        'docker/Dockerfile',
        'docker/docker-compose.yaml',
        '!tests/__init__.py',
        '!tests/app_test.py',
        '.github/workflows/build.yml',
    ],
    '-a gha -p flask -t pytest -l none -c none': [
        'src/project/__init__.py',
        'src/project/app.py',
        'src/project/config.py',
        'src/project/routes/__init__.py',
        'src/project/routes/root.py',
        'src/project/routes/api.py',
        'docker/Dockerfile',
        'docker/docker-compose.yaml',
        'tests/__init__.py',
        'tests/app_test.py',
        '.github/workflows/build.yml',
    ],
}


@pytest.mark.cli
@pytest.mark.parametrize('cmd', [*expected_files_for_config.keys()])
def test_cli_create(mock_configs, mock_update, mock_templates, cmd: str):
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
            *cmd.split(),
            '-s',
            'project',
        ])
        project_path = Path(f'{fs}/project')
        assert not result.exception
        assert project_path.exists()

        expected_files = [
            *common_files,
            *expected_files_for_config[cmd]
        ]
        for file_name in expected_files:
            if file_name[0] == '!':
                assert not (project_path / file_name[1:]).exists()
            else:
                assert (project_path / file_name).exists()


makefile_sections: Dict[str, str] = {
    'pytest': '.PHONY: test\ntest:  ## Runs the test suite\n\tpytest',
    'flake8': '.PHONY: lint fmt\nlint:  ## Runs the linter\n\tflake8',
    'mypy': '.PHONY: check\ncheck:  ## Runs the static type checker\n\tmypy',
}

expected_makefile_sections: Dict[str, List[str]] = {
    '-a none -l none -c none -p library -t none': [],
    '-a none -l flake8 -c none -p library -t none': ['flake8'],
    '-a none -l none -c mypy -p library -t none': ['mypy'],
    '-a none -l none -c none -p library -t pytest': ['pytest'],
    '-a none -l none -c mypy -p library -t pytest': ['mypy', 'pytest'],
    '-a none -l flake8 -c none -p library -t pytest': ['flake8', 'pytest'],
    '-a none -l flake8 -c mypy -p library -t none': ['flake8', 'mypy'],
    '-a none -l flake8 -c mypy -p library -t pytest': ['flake8', 'mypy', 'pytest'],
}


@pytest.mark.cli
@pytest.mark.parametrize('cmd', [*expected_makefile_sections.keys()])
def test_makefile(cmd: str):
    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        runner.invoke(cli.cli, [
            'create',
            '-n',
            'natalia',
            '-e',
            'email',
            *cmd.split(),
            '-s',
            'project',
        ])
        project_path = Path(f'{fs}/project')
        makefile = project_path / 'Makefile'
        assert makefile.exists()
        with open(makefile, 'r') as f:
            s = f.read().strip()
        for section, content in makefile_sections.items():
            if section in expected_makefile_sections[cmd]:
                assert content in s
            else:
                assert content not in s


@pytest.mark.cli
def test_cli_set_default():
    '''
    Tests that the set-default user interactions work appropriately
    '''

    runner = CliRunner()
    result = runner.invoke(cli.set_default)

    assert not result.exception
