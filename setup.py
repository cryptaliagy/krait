# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

with open('VERSION', 'r') as f:
    version = f.read().strip()

setup(
    name='krait',
    description='A Python CLI tool to create new python projects.',
    author='Natalia Maximo',
    author_email='iam@natalia.dev',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/taliamax/krait',
    license='Apache Software License',
    packages=find_packages(
        'src'
    ),
    extras_require={
        'tests': ['pytest-cov', 'flake8', 'mypy', 'pytest', 'types-setuptools'],
    },
    package_dir={'': 'src'},
    include_package_data=True,
    version=version,
    install_requires=[
        'click>=8.0', 'jinja2', 'pydeepmerge', 'gitpython'
    ],
    python_requires='>=3.7',
    keywords='cli project startup',
    entry_points={
        'console_scripts': ['krait = krait.cli:cli'],
        'krait.project_frameworks': [
            'click = krait.lib.plugins.project_frameworks:ClickFramework',
            'library = krait.lib.plugins.project_frameworks:LibraryProject',
            'flask = krait.lib.plugins.project_frameworks:FlaskProject',
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
            'azure = krait.lib.plugins.automations:AzurePipeline',
            'none = krait.lib.plugins.automations:NoAutomation',
        ],
        'krait.helplinks': [
            'krait = krait.lib.plugins.help_links:KraitHelpLinks',
        ],
        'krait.vcs': [
            'git = krait.lib.plugins.vcs:GitPlugin',
            'none = krait.lib.plugins.vcs:NoVCS',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
)
