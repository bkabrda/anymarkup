# -*- coding: utf-8 -*-
import io
import os

import pytest
import six

from anymarkup import *

from test import *


class TestSerialize(object):
    fixtures = os.path.join(os.path.dirname(__file__), 'fixtures')

    def _read_decode(self, file):
        if isinstance(file, six.string_types):
            file = open(file, 'rb')
        else:
            file.seek(0)
        return file.read().decode('utf-8')

    @pytest.mark.parametrize('struct, format, expected', [
        (example_ini_as_struct, 'ini', example_ini),
        (example_as_struct, 'json', example_json),
        (example_as_struct, 'xml', example_xml),
        # TODO: figure out how to serialize OrderedDict by PyYAML
        #(example_as_struct, 'yaml', example_yaml),
    ])
    def test_serialize_basic(self, struct, format, expected):
        serialized = serialize(struct, format)
        assert serialized == expected.encode('utf-8')

    def test_serialize_works_with_wb_opened_file(self, tmpdir):
        f = os.path.join(str(tmpdir), 'foo.json')
        fhandle = open(f, 'wb+')
        serialize(example_as_struct, 'json', fhandle)
        assert self._read_decode(fhandle) == example_json

    def test_serialize_raises_with_unicode_opened_file(self, tmpdir):
        # on Python 2, this can only be simulated with io.open
        f = os.path.join(str(tmpdir), 'foo.json')
        fhandle = io.open(f, 'w+', encoding='utf-8')
        with pytest.raises(AnyMarkupError):
            serialize(example_as_struct, 'json', fhandle)

    @pytest.mark.parametrize('struct, fname, expected', [
        (example_ini_as_struct, 'example.ini', example_ini),
        (example_as_struct, 'example.json', example_json),
        (example_as_struct, 'example.xml', example_xml),
        # TODO: OrderedDict/PyYAML
        #(example_as_struct, 'example.yaml', example_yaml),
    ])
    def test_serialize_file_basic(self, struct, fname, expected, tmpdir):
        f = os.path.join(str(tmpdir), fname)
        serialize_file(struct, f)
        assert self._read_decode(f) == expected

    def test_serialize_file_format_overrides_extension(self, tmpdir):
        f = os.path.join(str(tmpdir), 'foo.ini')
        serialize_file(example_as_struct, f, 'json')
        assert self._read_decode(f) == example_json
