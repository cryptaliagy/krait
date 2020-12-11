# Krait – CLI for setting up new python projects

[![Build status badge](https://img.shields.io/github/workflow/status/taliamax/krait/build)](https://github.com/taliamax/krait/actions?query=workflow%3Abuild)
[![PyPI version badge](https://img.shields.io/pypi/v/krait)](https://pypi.org/project/krait/)
[![PyPI Status Badge](https://img.shields.io/pypi/status/krait)](https://pypi.org/project/krait/)
[![Python versions badge](https://img.shields.io/pypi/pyversions/krait)](https://github.com/taliamax/krait)
[![License](https://img.shields.io/github/license/taliamax/krait)](https://github.com/taliamax/krait/blob/master/LICENSE)
[![Downloads per month](https://img.shields.io/pypi/dm/krait)](https://pypi.org/project/krait/)

Welcome to Krait!

Krait is a python-built CLI for new python projects! Working on new code usually means setting up linters, type checkers, testing frameworks, and/or automations, but how often do those things get worked on?

I made Krait to solve the issue of starting up new python projects rapidly while ensuring that code quality is high. By baking these tools into the project creation process, you can find mistakes and issues early on and save time debugging.

Krait is currently in Beta, and new features are still being worked on. A few of the features coming soon:

- Git integration, allowing new projects to already be initialized repositories
- Saving preferred name and email for new project startup
- Pre-commit hooks
- Support for creating projects with Flask

Documentation is also being worked on to explain the process of extending Krait by writing your own plugins. This would allow external packages to enhance the number of options permitted for each of the tools that we support


## Installation

Simplest installation is through pip.

```bash
$ pip install krait
```
