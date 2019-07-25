# -*- coding: utf-8 -*-
from anymarkup.cli import cli
from click.testing import CliRunner
import pytest

from .data import TEST_DATA_INI, TEST_DATA_INI_INTERPOLATION


@pytest.fixture(scope="class")
def runner():
    return CliRunner()


# Testing conversion from INI
class TestConversionFromIni():
    def test_convert_no_error(self, runner):
        arguments = [
            ['convert'],
            ['convert', '--from-format', 'ini'],
            ['convert', '--from-format', 'ini', '--to-format', 'ini'],
            ['convert', '--from-format', 'ini', '--to-format', 'json'],
            ['convert', '--from-format', 'ini', '--to-format', 'json5'],
            ['convert', '--from-format', 'ini', '--to-format', 'toml'],
            ['convert', '--from-format', 'ini', '--to-format', 'xml'],
            ['convert', '--from-format', 'ini', '--to-format', 'yaml']
        ]
        for args in arguments:
            result = runner.invoke(cli, args, input=TEST_DATA_INI)
            assert result.exit_code == 0
            assert not result.exception

    def test_wrong_input_format(self, runner):
        arguments = [
            ['convert', '--from-format', 'json'],
            ['convert', '--from-format', 'json5'],
            ['convert', '--from-format', 'toml'],
            ['convert', '--from-format', 'xml'],
            ['convert', '--from-format', 'yaml'],
        ]
        for args in arguments:
            result = runner.invoke(cli, args, input=TEST_DATA_INI)
            assert result.exit_code != 0
            assert result.exception

    def test_interpolation_in_file_fail(self, runner):
        arguments = [
            ['convert', '--from-format', 'ini'],
            ['convert', '--from-format', 'json'],
            ['convert', '--from-format', 'json5'],
            ['convert', '--from-format', 'toml'],
            ['convert', '--from-format', 'xml'],
            ['convert', '--from-format', 'yaml'],
        ]
        for args in arguments:
            result = runner.invoke(cli, args, input=TEST_DATA_INI_INTERPOLATION)
            assert result.exit_code != 0
            assert result.exception

    def test_convert_interpolation_option_fail(self, runner):
        arguments = [
            ['convert', '--interpolate'],
            ['convert', '--interpolate', '--from-format', 'ini'],
            ['convert', '--interpolate', '--from-format', 'ini', '--to-format', 'ini'],
            ['convert', '--interpolate', '--from-format', 'ini', '--to-format', 'json'],
            ['convert', '--interpolate', '--from-format', 'ini', '--to-format', 'json5'],
            ['convert', '--interpolate', '--from-format', 'ini', '--to-format', 'toml'],
            ['convert', '--interpolate', '--from-format', 'ini', '--to-format', 'xml'],
            ['convert', '--interpolate', '--from-format', 'ini', '--to-format', 'yaml']
        ]
        for args in arguments:
            result = runner.invoke(cli, args, input=TEST_DATA_INI_INTERPOLATION)
            assert result.exit_code != 0
            assert result.exception

    def test_convert_interpolation_off_no_error(self, runner):
        arguments = [
            ['convert', '--no-interpolate'],
            ['convert', '--no-interpolate', '--from-format', 'ini'],
            ['convert', '--no-interpolate', '--from-format', 'ini', '--to-format', 'ini'],
            ['convert', '--no-interpolate', '--from-format', 'ini', '--to-format', 'json'],
            ['convert', '--no-interpolate', '--from-format', 'ini', '--to-format', 'json5'],
            ['convert', '--no-interpolate', '--from-format', 'ini', '--to-format', 'toml'],
            ['convert', '--no-interpolate', '--from-format', 'ini', '--to-format', 'xml'],
            ['convert', '--no-interpolate', '--from-format', 'ini', '--to-format', 'yaml']
        ]
        for args in arguments:
            result = runner.invoke(cli, args, input=TEST_DATA_INI_INTERPOLATION)
            assert result.exit_code == 0
            assert not result.exception