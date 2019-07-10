# -*- coding: utf-8 -*-
from anymarkup.cli import cli
from click.testing import CliRunner
import pytest

from .data import TEST_DATA_JSON


@pytest.fixture(scope="class")
def runner():
    return CliRunner()


# Testing conversion from JSON
class TestConversionFromJson():
    def test_convert_no_error(self, runner):
        arguments = [
            ['convert'],
            ['convert', '--from-format', 'json'],
            ['convert', '--from-format', 'json', '--to-format', 'ini'],
            ['convert', '--from-format', 'json', '--to-format', 'json'],
            ['convert', '--from-format', 'json', '--to-format', 'json5'],
            ['convert', '--from-format', 'json', '--to-format', 'toml'],
            ['convert', '--from-format', 'json', '--to-format', 'xml'],
            ['convert', '--from-format', 'json', '--to-format', 'yaml']
        ]
        for args in arguments:
            result = runner.invoke(cli, args, input=TEST_DATA_JSON)
            assert result.exit_code == 0
            assert not result.exception

    def test_wrong_input_format_still_works(self, runner):
        arguments = [
            ['convert', '--from-format', 'json5'],
            ['convert', '--from-format', 'yaml'],
        ]
        for args in arguments:
            result = runner.invoke(cli, args, input=TEST_DATA_JSON)
            assert result.exit_code == 0
            assert not result.exception

    def test_wrong_input_format(self, runner):
        arguments = [
            ['convert', '--from-format', 'ini'],
            ['convert', '--from-format', 'toml'],
            ['convert', '--from-format', 'xml'],
        ]
        for args in arguments:
            result = runner.invoke(cli, args, input=TEST_DATA_JSON)
            assert result.exit_code != 0
            assert result.exception
