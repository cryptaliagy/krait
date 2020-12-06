# -*- coding: utf-8 -*-
import pytest
import project.main as main

from click.testing import CliRunner


@pytest.mark.cli
def test_cli():
    '''
    Tests that the actual CLI works as expected. As the project
    develops, new tests are likely to be required, such as passing
    in some standard data to make sure it works appropriately.

    For now, this just checks that running the CLI does not produce
    an exception.
    '''

    runner = CliRunner()
    result = runner.invoke(main.main)

    assert not result.exception
