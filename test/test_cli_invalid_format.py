# -*- coding: utf-8 -*-
from anymarkup.cli import cli
from click.testing import CliRunner
import pytest

from .data import *


@pytest.fixture(scope="class")
def runner():
    return CliRunner()


# Testing INI parsing against other file formats
class TestCliInvalidInputFormatIni():
    def test_convert_valid_ini_file_from_toml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'ini'], input=TEST_DATA_TOML)
        assert result.exit_code == 0
        assert not result.exception

    def test_convert_invalid_ini_file_from_json(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'ini'], input=TEST_DATA_JSON)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_ini_file_from_json5(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'ini'], input=TEST_DATA_JSON5)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_ini_file_from_yaml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'ini'], input=TEST_DATA_YAML)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_ini_file_from_xml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'ini'], input=TEST_DATA_XML)
        assert result.exit_code != 0
        assert result.exception


# Testing JSON parsing against other file formats
class TestCliInvalidInputFormatJson():
    def test_convert_valid_json_file_from_json5(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'json'], input=TEST_DATA_JSON5)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_json_file_from_ini(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'json'], input=TEST_DATA_INI)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_json_file_from_toml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'json'], input=TEST_DATA_TOML)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_json_file_from_yaml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'json'], input=TEST_DATA_YAML)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_json_file_from_xml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'json'], input=TEST_DATA_XML)
        assert result.exit_code != 0
        assert result.exception


# Testing JSON5 parsing against other file formats
class TestCliInvalidInputFormatJson5():
    def test_convert_valid_json5_file_from_json(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'json5'], input=TEST_DATA_JSON)
        assert result.exit_code == 0
        assert not result.exception

    def test_convert_invalid_json5_file_from_ini(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'json5'], input=TEST_DATA_INI)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_json5_file_from_toml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'json5'], input=TEST_DATA_TOML)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_json5_file_from_yaml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'json5'], input=TEST_DATA_YAML)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_json5_file_from_xml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'json5'], input=TEST_DATA_XML)
        assert result.exit_code != 0
        assert result.exception


# Testing TOML parsing against other file formats
class TestCliInvalidInputFormatToml():
    def test_convert_invalid_toml_file_from_ini(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'toml'], input=TEST_DATA_INI)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_toml_file_from_json(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'toml'], input=TEST_DATA_JSON)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_toml_file_from_json5(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'toml'], input=TEST_DATA_JSON5)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_toml_file_from_yaml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'toml'], input=TEST_DATA_YAML)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_toml_file_from_xml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'toml'], input=TEST_DATA_XML)
        assert result.exit_code != 0
        assert result.exception


# Testing YAML parsing against other file formats
class TestCliInvalidInputFormatYaml():
    def test_convert_valid_yaml_file_from_json(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'yaml'], input=TEST_DATA_JSON)
        assert result.exit_code == 0
        assert not result.exception

    def test_convert_valid_yaml_file_from_json5(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'yaml'], input=TEST_DATA_JSON5)
        assert result.exit_code == 0
        assert not result.exception

    def test_convert_invalid_yaml_file_from_ini(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'yaml'], input=TEST_DATA_INI)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_yaml_file_from_toml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'yaml'], input=TEST_DATA_TOML)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_yaml_file_from_xml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'yaml'], input=TEST_DATA_XML)
        assert result.exit_code != 0
        assert result.exception


# Testing Xml parsing against other file formats
class TestCliInvalidInputFormatXml():
    def test_convert_invalid_xml_file_from_ini(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'xml'], input=TEST_DATA_INI)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_xml_file_from_json(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'xml'], input=TEST_DATA_JSON)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_xml_file_from_json5(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'xml'], input=TEST_DATA_JSON5)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_xml_file_from_xml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'xml'], input=TEST_DATA_TOML)
        assert result.exit_code != 0
        assert result.exception

    def test_convert_invalid_xml_file_from_yaml(self, runner):
        result = runner.invoke(cli, ['convert', '--from-format', 'xml'], input=TEST_DATA_YAML)
        assert result.exit_code != 0
        assert result.exception

