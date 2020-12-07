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
        'console_scripts': ['krait = krait.main:main'],
        'krait.cli_frameworks': [
            'click = krait.lib.cli_frameworks:ClickFramework'
        ],
        'krait.linters': [
            'flake8 = krait.lib.linters:Flake8'
        ],
        'krait.type_checkers': [
            'mypy = krait.lib.type_checkers:MyPy'
        ],
        'krait.test_frameworks': [
            'pytest = krait.lib.test_frameworks:Pytest'
        ],
        'krait.automations': [
            'gha = krait.lib.automations:GithubActions'
        ],
    },
)
