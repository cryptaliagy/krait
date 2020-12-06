# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().split('\n')

setup(
    name='krait',
    author='Natalia Maximo',
    author_email='iam@natalia.dev',
    packages=find_packages(
        'src'
    ),
    package_dir={'': 'src'},
    version='0.1a',
    install_requires=requirements,
    entry_points={
        'console_scripts': ['krait = krait.main:main']
    },
)
