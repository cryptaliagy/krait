# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='krait',
    description='A Python CLI tool to create new python projects.',
    author='Natalia Maximo',
    author_email='iam@natalia.dev',
    packages=find_packages(
        'src'
    ),
    package_dir={'': 'src'},
    include_package_data=True,
    version='0.1a0',
    install_requires=[
        'click', 'jinja2'
    ],
    entry_points={
        'console_scripts': ['krait = krait.cli:cli'],
        'krait.cli_frameworks': [
            'click = krait.lib.plugins.cli_frameworks:ClickFramework',
            'none = krait.lib.plugins.cli_frameworks:NoCliFramework',
        ],
        'krait.linters': [
            'flake8 = krait.lib.plugins.linters:Flake8',
            'none = krait.lib.plugins.linters:NoLinter',
        ],
        'krait.type_checkers': [
            'mypy = krait.lib.plugins.type_checkers:MyPy',
            'none = krait.lib.plugins.type_checkers:NoTypeChecker',
        ],
        'krait.test_frameworks': [
            'pytest = krait.lib.plugins.test_frameworks:Pytest',
            'none = krait.lib.plugins.test_frameworks:NoTesting',
        ],
        'krait.automations': [
            'gha = krait.lib.plugins.automations:GithubActions',
            'none = krait.lib.plugins.automations:NoAutomation'
        ],
    },
)
