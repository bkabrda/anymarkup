# -*- coding: utf-8 -*-
from anymarkup.cli import cli
from click.testing import CliRunner
import pytest

from .data import TEST_DATA_XML


@pytest.fixture(scope="class")
def runner():
    return CliRunner()


# Testing conversion from XML
class TestConversionFromXml():
    def test_convert_no_error(self, runner):
        arguments = [
            ['convert'],
            ['convert', '--from-format', 'xml'],
            ['convert', '--from-format', 'xml', '--to-format', 'ini'],
            ['convert', '--from-format', 'xml', '--to-format', 'json'],
            ['convert', '--from-format', 'xml', '--to-format', 'json5'],
            ['convert', '--from-format', 'xml', '--to-format', 'toml'],
            ['convert', '--from-format', 'xml', '--to-format', 'xml'],
            ['convert', '--from-format', 'xml', '--to-format', 'yaml']
        ]

        for args in arguments:
            result = runner.invoke(cli, args, input=TEST_DATA_XML)
            assert result.exit_code == 0
            assert not result.exception

    def test_wrong_input_format(self, runner):
        arguments = [
            ['convert', '--from-format', 'ini'],
            ['convert', '--from-format', 'json'],
            ['convert', '--from-format', 'json5'],
            ['convert', '--from-format', 'toml'],
            ['convert', '--from-format', 'yaml'],
        ]

        for args in arguments:
            result = runner.invoke(cli, args, input=TEST_DATA_XML)
            assert result.exit_code != 0
            assert result.exception
