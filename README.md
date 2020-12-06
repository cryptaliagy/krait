# Python Startup Template Repository!

![Build status badge](https://img.shields.io/github/workflow/status/taliamax/starter_python/build)
![MIT License badge](https://img.shields.io/github/license/taliamax/starter_python)
![Github repository size](https://img.shields.io/github/repo-size/taliamax/starter_python)

Starting up new projects, especially command-line applications, can often be tedious. It's hard to remember all of the tools that are used to speed up development and how they're properly configured. This repository allows that step to be recycled by providing a starter CLI with everything needed out of the box, including testing automation through Github Actions.

### Table of Contents
1. [License](#License)
1. [What to edit first](#What-to-edit-first)
1. [Installation](#Installation)
1. [What are all these tools??](#What-are-all-these-tools)
1. [Extra documentation](#Extra-documentation)

## License
This repository is offered under an MIT license and is free to be used however one might prefer

## What to edit first
You'll most likely want to name things differently. The most glaring example is how the term 'project' is used here as the name of the application. I have tried to minimize the number of places where it is used to make it easier to adapt this repository to different needs. You should edit the following, ensuring that all have the same new name:

- The `project` directory, naming it as makes sense for your project
- Inside the `tests/cli_test.py` file, edit the following line:
    - `import project.main as main`
- Inside the `setup.cfg` file, edit the following lines:
    - `addopts = --cov=project --cov-report term-missing`
    - `files = project/**/*.py`
- Inside the `setup.py` file:
    - `name='project'`
    - `'console_scripts': ['project = project.main:main']`

## Installation
To install, run the convenience script included with this repository or execute the following code below in your terminal. It is highly recommended that a virtual environment is used for this (and all) Python applications.

```sh
pip install -r requirements.txt -r test-requirements.txt -e .;
pre-commit install;
pre-commit run --all-files;
mypy;
pytest;
```


## What are all these tools??
`pre-commit` is a tool used to run a series of checks before `git commit` is finished executing. This may seem cumbersome or annoying, but it'll often catch little mistakes that degrade code quality over time. Quite a few of the checks that it runs will also fix the problems that they are checking for.

`flake8` is a linter. You can read some more about linters [here](https://en.wikipedia.org/wiki/Lint_(software)).
Also check out their [repository](https://gitlab.com/pycqa/flake8) and their [documentation](https://flake8.pycqa.org/en/latest/)

`mypy` is a static type analyzer. Python is a dynamically typed language, and `mypy` doesn't seek to change that. However, they do hope to add some of the benefits of static typing, such as legibility. It's a fairly popular tool, and you can read some of its benefits [here](https://dropbox.tech/application/our-journey-to-type-checking-4-million-lines-of-python). If you're new to python type hints (they were introduced in Python 3.5), check out the [docs](https://docs.python.org/3/library/typing.html)

`pytest` is a popular python testing framework. It has good outputs and plenty of plugins, including a coverage report to see how much of your code is covered by tests.


## Extra documentation
The following links might be helpful:
- [Click Quickstart](https://click.palletsprojects.com/en/7.x/quickstart/)
- [Pytest docs](https://docs.pytest.org/en/stable/contents.html)
- [Pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Parametrizing tests](https://docs.pytest.org/en/stable/example/parametrize.html)
