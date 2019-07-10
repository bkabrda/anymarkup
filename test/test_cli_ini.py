# -*- coding: utf-8 -*-
from anymarkup.cli import cli
from click.testing import CliRunner
import pytest

from .data import *


@pytest.fixture(scope="class")
def runner():
    return CliRunner()


# Testing conversion from INI
class TestConversionFromIni():
    def test_convert_ini_no_format_options(self, runner):
        result = runner.invoke(cli, ['convert'], input=TEST_DATA_INI)
        assert result.exit_code == 0
        assert not result.exception
        assert str(result.output) == TEST_DATA_JSON

    def test_convert_ini_to_ini(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'ini', '--to-format', 'ini'], input=TEST_DATA_INI)
        assert result.exit_code == 0
        assert not result.exception
        assert str(result.output) == TEST_DATA_INI

    def test_convert_ini_to_json(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'ini', '--to-format', 'json'], input=TEST_DATA_INI)
        assert result.exit_code == 0
        assert not result.exception
        assert str(result.output) == TEST_DATA_JSON

    def test_convert_ini_to_json5(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'ini', '--to-format', 'json5'], input=TEST_DATA_INI)
        assert result.exit_code == 0
        assert not result.exception
        assert str(result.output) == TEST_DATA_JSON5

    def test_convert_ini_to_toml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'ini', '--to-format', 'toml'], input=TEST_DATA_INI)
        assert result.exit_code == 0
        assert not result.exception
        assert str(result.output) == TEST_DATA_TOML_WITHOUT_EMPTY

    def test_convert_ini_to_xml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'ini', '--to-format', 'xml'], input=TEST_DATA_INI)
        assert result.exit_code == 0
        assert not result.exception
        assert str(result.output) == TEST_DATA_XML

    def test_convert_ini_to_yaml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'ini', '--to-format', 'yaml'], input=TEST_DATA_INI)
        assert result.exit_code == 0
        assert not result.exception
        assert str(result.output).strip() == TEST_DATA_YAML_SORTED
