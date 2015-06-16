# -*- coding: utf-8 -*-
import io
import os

import pytest
import six

from anymarkup import *

from test import *


class TestParse(object):
    fixtures = os.path.join(os.path.dirname(__file__), 'fixtures')

    def assert_unicode(self, struct):
        if isinstance(struct, dict):
            for k, v in struct.items():
                self.assert_unicode(k)
                self.assert_unicode(v)
        elif isinstance(struct, list):
            for i in struct:
                self.assert_unicode(i)
        elif isinstance(struct, (six.string_types, type(None), type(True), \
                six.integer_types, float)):
            pass
        else:
            raise AssertionError('Unexpected type {0} in parsed structure'.format(type(struct)))

    @pytest.mark.parametrize(('str', 'expected'), [
        ('', {}),
        ('{}', {}),
        ('[]', []),
        (example_ini, example_as_dict),
        (example_json, example_as_dict),
        (example_xml, example_as_ordered_dict),
        (example_yaml_map, example_as_dict),
        (example_yaml_omap, example_as_ordered_dict),
    ])
    def test_parse_basic(self, str, expected):
        parsed = parse(str)
        assert parsed == expected
        assert type(parsed) == type(expected)
        self.assert_unicode(parsed)

    @pytest.mark.parametrize(('str', 'expected'), [
        ('# comment', {}),
        ('# comment\n', {}),
        ('# comment\n' + example_ini, example_as_dict),
        ('# comment\n' + example_json, example_as_dict),
        ('# comment\n' + example_yaml_map, example_as_dict),
        ('# comment\n' + example_yaml_omap, example_as_ordered_dict),
    ])
    def test_parse_recognizes_comments_in_ini_json_yaml(self, str, expected):
        parsed = parse(str)
        assert parsed == expected
        assert type(parsed) == type(expected)
        self.assert_unicode(parsed)

    @pytest.mark.parametrize('str', [
        types_ini,
        types_json,
        types_xml,
        types_yaml,
    ])
    def test_parse_force_types_true(self, str):
        assert parse(str) == types_as_struct_with_objects

    @pytest.mark.parametrize('str', [
        types_ini,
        types_json,
        types_xml,
        types_yaml,
    ])
    def test_parse_force_types_false(self, str):
        assert parse(str, force_types=False) == types_as_struct_with_strings

    @pytest.mark.parametrize(('str', 'expected'), [
        # Note: the expected result is backend-specific
        (types_ini, {'x': {'a': '1', 'b': '1.1', 'c': 'None', 'd': 'True'}}),
        (types_json, {'x': {'a': 1, 'b': 1.1, 'c': None, 'd': True}}),
        (types_xml, {'x': {'a': '1', 'b': '1.1', 'c': 'None', 'd': 'True'}}),
        (types_yaml, {'x': {'a': 1, 'b': 1.1, 'c': 'None', 'd': True}}),
    ])
    def test_parse_force_types_none(self, str, expected):
        assert parse(str, force_types=None) == expected

    def test_parse_works_with_bytes_yielding_file(self):
        f = open(os.path.join(self.fixtures, 'empty.ini'), 'rb')
        parsed = parse(f)
        assert parsed == {}

    def test_parse_works_with_unicode_yielding_file(self):
        # on Python 2, this can only be simulated with io.open
        f = io.open(os.path.join(self.fixtures, 'empty.ini'), encoding='utf-8')
        parsed = parse(f)
        assert parsed == {}

    def test_parse_fails_on_wrong_format(self):
        with pytest.raises(AnyMarkupError):
            parse('foo: bar', format='xml')

    @pytest.mark.parametrize(('file', 'expected'), [
        # TODO: some parsers allow empty files, others don't - this should be made consistent
        ('empty.ini', {}),
        ('empty.json', AnyMarkupError),
        ('empty.xml', AnyMarkupError),
        ('empty.yaml', {}),
        ('example.ini', example_as_dict),
        ('example.json', example_as_dict),
        ('example.xml', example_as_ordered_dict),
        ('example.yaml', example_as_dict),
    ])
    def test_parse_file_basic(self, file, expected):
        f = os.path.join(self.fixtures, file)
        if expected == AnyMarkupError:
            with pytest.raises(AnyMarkupError):
                parse_file(f)
        else:
            parsed = parse_file(f)
            assert parsed == expected
            self.assert_unicode(parsed)

    def test_parse_file_noextension(self):
        parsed = parse_file(os.path.join(self.fixtures, 'without_extension'))
        assert parsed == example_as_dict
        self.assert_unicode(parsed)

    def test_parse_file_fails_on_bad_extension(self):
        with pytest.raises(AnyMarkupError):
            parse_file(os.path.join(self.fixtures, 'bad_extension.xml'))

    def test_parse_file_respects_force_types(self):
        f = os.path.join(self.fixtures, 'types.json')
        parsed = parse_file(f, force_types=True)
        assert parsed == {'a': 1, 'b': 1}
        parsed = parse_file(f, force_types=False)
        assert parsed == {'a': '1', 'b': '1'}
        parsed = parse_file(f, force_types=None)
        assert parsed == {'a': 1, 'b': '1'}
