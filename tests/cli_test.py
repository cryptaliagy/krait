# -*- coding: utf-8 -*-
import pytest
import krait.main as main

from click.testing import CliRunner


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
    result = runner.invoke(main.create)

    assert not result.exception


@pytest.mark.cli
def test_cli_set_default():
    '''
    Tests that the set-default user interactions work appropriately
    '''

    runner = CliRunner()
    result = runner.invoke(main.set_default)

    assert not result.exception
