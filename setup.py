# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='krait',
    author='Natalia Maximo',
    author_email='iam@natalia.dev',
    packages=find_packages(
        'src'
    ),
    package_dir={'': 'src'},
    version='0.1a',
    install_requires=[
        'click'
    ],
    entry_points={
        'console_scripts': ['krait = krait.main:main']
    },
)
