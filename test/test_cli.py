# -*- coding: utf-8 -*-
from anymarkup import __version__
from anymarkup.cli import cli
from click.testing import CliRunner
import pytest


@pytest.fixture(scope="class")
def runner():
    return CliRunner()


# Testing the CLI outside the conversion arguments
class TestCli():
    def test_no_arguments(self, runner):
        result = runner.invoke(cli)
        assert result.exit_code == 0
        assert not result.exception

    def test_invalid_command(self, runner):
        result = runner.invoke(cli, ['--foobar'])
        assert result.exit_code != 0
        assert result.exception

    def test_help(self, runner):
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert not result.exception

    def test_convert_help(self, runner):
        result = runner.invoke(cli, ['convert', '--help'])
        assert result.exit_code == 0
        assert not result.exception

    def test_version(self, runner):
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert not result.exception
        assert result.output == 'anymarkup, version ' + __version__ + '\n'

    def test_convert_invalid_file(self, runner):
        result = runner.invoke(cli, ['convert', 'foobar'])
        assert result.exit_code != 0
        assert result.exception
