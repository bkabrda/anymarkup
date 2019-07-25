# -*- coding: utf-8 -*-
import anymarkup
import sys
import click


@click.version_option(version=anymarkup.__version__, prog_name='anymarkup')
@click.group()
def cli():
    """
    anymarkup - Converts markup files from one format to another. Supports ini, json, json5, toml, xml and yaml.
    Source available at: https://github.com/bkabrda/anymarkup

    More help available by running: anymarkup convert --help
    """


@cli.command('convert')
@click.argument('filename', type=click.File('r'), default='-')
@click.option('-f', '--from-format', type=click.Choice(['ini', 'json', 'json5', 'toml', 'yaml', 'xml']), default=None,
              help='Input file format, if not specified, an educated guess will be made')
@click.option('-t', '--to-format', type=click.Choice(['ini', 'json', 'json5', 'toml', 'yaml', 'xml']), default='json',
              help='Output format to serialize to, the default is JSON')
@click.option('--interpolate/--no-interpolate', default=True,
              help='Whether to interpolate strings, the default is True')
def convert(filename, from_format, to_format, interpolate):
    """Parses stdin or a file and converts to the specified format"""

    # Try to parse the file and output in the specified format
    data = anymarkup.parse(filename, format=from_format, interpolate=interpolate)
    serialized = anymarkup.serialize(data, format=to_format)
    click.echo(serialized)

    # Exit if all done
    sys.exit(0)


if __name__ == '__main__':
    cli(prog_name='anymarkup')