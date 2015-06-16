# -*- coding: utf-8 -*-
import io
import os

import pytest
import six

from anymarkup import *

from test import *


class TestSerialize(object):
    """Note: testing serialization is a bit tricky, since serializing dicts can result
    in different order of values in serialized string in different runs.
    That means that we can't just test whether the serialized string equals to expected
    string. To solve this, we rather parse the serialized string back and make sure
    that it equals the original structure.
    """

    fixtures = os.path.join(os.path.dirname(__file__), 'fixtures')

    def _read_decode(self, file):
        if isinstance(file, six.string_types):
            file = open(file, 'rb')
        else:
            file.seek(0)
        return file.read().decode('utf-8')

    @pytest.mark.parametrize(('struct', 'format'), [
        (example_as_dict, 'ini'),
        (example_as_dict, 'json'),
        (example_as_ordered_dict, 'xml'),
        (example_as_dict, 'yaml'),
        (example_as_ordered_dict, 'yaml'),
    ])
    def test_serialize_basic(self, struct, format):
        serialized = serialize(struct, format)
        parsed_back = parse(serialized)
        assert parsed_back == struct
        assert type(parsed_back) == type(struct)

    def test_serialize_works_with_wb_opened_file(self, tmpdir):
        f = os.path.join(str(tmpdir), 'foo.xml')
        fhandle = open(f, 'wb+')
        serialize(example_as_ordered_dict, 'xml', fhandle)
        assert self._read_decode(fhandle) == example_xml

    def test_serialize_raises_with_unicode_opened_file(self, tmpdir):
        # on Python 2, this can only be simulated with io.open
        f = os.path.join(str(tmpdir), 'foo.json')
        fhandle = io.open(f, 'w+', encoding='utf-8')
        with pytest.raises(AnyMarkupError):
            serialize(example_as_dict, 'json', fhandle)

    @pytest.mark.parametrize(('struct', 'fname'), [
        (example_as_dict, 'example.ini'),
        (example_as_dict, 'example.json'),
        (example_as_ordered_dict, 'example.xml'),
        (example_as_dict, 'example.yaml'),
        (example_as_ordered_dict, 'example_ordered.yaml'),
    ])
    def test_serialize_file_basic(self, struct, fname, tmpdir):
        f = os.path.join(str(tmpdir), fname)
        serialize_file(struct, f)
        parsed_back = parse(self._read_decode(f))
        assert parsed_back == struct
        assert type(parsed_back) == type(struct)

    def test_serialize_file_format_overrides_extension(self, tmpdir):
        f = os.path.join(str(tmpdir), 'foo.ini')
        serialize_file(example_as_dict, f, 'json')
        assert parse(self._read_decode(f)) == example_as_dict
