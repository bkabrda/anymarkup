# -*- coding: utf-8 -*-
import collections
import io
import json
import os
import re

import configobj
import six
import xmltodict
import yaml


__all__ = ['AnyMarkupError', 'parse', 'parse_file', 'serialize', 'serialize_file']
__version__ = '0.4.3'


fmt_to_exts = {'ini': ['ini'], 'json': ['json'], 'xml': ['xml'], 'yaml': ['yaml', 'yml']}


class AnyMarkupError(Exception):
    def __init__(self, cause):
        """Wrapper for all errors that occur during anymarkup calls.

        Args:
            cause: either a reraised exception or a string with cause
        """
        super(AnyMarkupError, self).__init__()
        self.cause = cause

    def __str__(self):
        cause = str(self.cause)
        if isinstance(self.cause, Exception):
            cause = 'caught {0}: {1}'.format(type(self.cause), cause)
        return 'AnyMarkupError: {0}'.format(cause)


def parse(inp, format=None, encoding='utf-8', force_types=True):
    """Parse input from file-like object, unicode string or byte string.

    Args:
        inp: file-like object, unicode string or byte string with the markup
        format: explicitly override the guessed `inp` markup format
        encoding: `inp` encoding, defaults to utf-8
        force_types:
            if `True`, integers, floats, booleans and none/null
                are recognized and returned as proper types instead of strings;
            if `False`, everything is converted to strings
            if `None`, backend return value is used
    Returns:
        parsed input (dict or list) containing unicode values
    Raises:
        AnyMarkupError if a problem occurs while parsing or inp
    """
    proper_inp = inp
    if hasattr(inp, 'read'):
        proper_inp = inp.read()
    # if proper_inp is unicode, encode it
    if isinstance(proper_inp, six.text_type):
        proper_inp = proper_inp.encode(encoding)

    # try to guess markup type
    fname = None
    if hasattr(inp, 'name'):
        fname = inp.name
    fmt = _get_format(format, fname, proper_inp)

    # make it look like file-like bytes-yielding object
    proper_inp = six.BytesIO(proper_inp)

    try:
        res = _do_parse(proper_inp, fmt, encoding, force_types)
    except Exception as e:
        # I wish there was only Python 3 and I could just use "raise ... from e"
        raise AnyMarkupError(e)
    if res is None:
        res = {}

    return res


def parse_file(path, format=None, encoding='utf-8', force_types=True):
    """A convenience wrapper of parse, which accepts path of file to parse.

    Args:
        path: path to file to parse
        format: explicitly override the guessed `inp` markup format
        encoding: file encoding, defaults to utf-8
        force_types:
            if `True`, integers, floats, booleans and none/null
                are recognized and returned as proper types instead of strings;
            if `False`, everything is converted to strings
            if `None`, backend return value is used
    Returns:
        parsed `inp` (dict or list) containing unicode values
    Raises:
        AnyMarkupError if a problem occurs while parsing
    """
    try:
        with open(path, 'rb') as f:
            return parse(f, format, encoding, force_types)
    except EnvironmentError as e:
        raise AnyMarkupError(e)


def serialize(struct, format, target=None, encoding='utf-8'):
    """Serialize given structure and return it as encoded string or write it to file-like object.

    Args:
        struct: structure (dict or list) with unicode members to serialize; note that list
            can only be serialized to json
        format: specify markup format to serialize structure as
        target: binary-opened file-like object to serialize to; if None (default),
            the result will be returned instead of writing to `target`
        encoding: encoding to use when serializing, defaults to utf-8
    Returns:
        bytestring with serialized structure if `target` is None; return value of
        `target.write` otherwise
    Raises:
        AnyMarkupError if a problem occurs while serializing
    """
    # raise if "unicode-opened"
    if hasattr(target, 'encoding') and target.encoding:
        raise AnyMarkupError('Input file must be opened in binary mode')

    fname = None
    if hasattr(target, 'name'):
        fname = target.name

    fmt = _get_format(format, fname)
    serialized = _do_serialize(struct, fmt, encoding)
    try:
        if target is None:
            return serialized
        else:
            return target.write(serialized)
    except Exception as e:
        raise AnyMarkupError(e)


def serialize_file(struct, path, format=None, encoding='utf-8'):
    """A convenience wrapper of serialize, which accepts path of file to serialize to.

    Args:
        struct: structure (dict or list) with unicode members to serialize; note that list
            can only be serialized to json
        path: path of the file to serialize to
        format: override markup format to serialize structure as (taken from filename
            by default)
        encoding: encoding to use when serializing, defaults to utf-8
    Returns:
        number of bytes written
    Raises:
        AnyMarkupError if a problem occurs while serializing
    """
    try:
        with open(path, 'wb') as f:
            return serialize(struct, format, f, encoding)
    except EnvironmentError as e:
        raise AnyMarkupError(e)


def _do_parse(inp, fmt, encoding, force_types):
    """Actually parse input.

    Args:
        inp: bytes yielding file-like object
        fmt: format to use for parsing
        encoding: encoding of `inp`
        force_types:
            if `True`, integers, floats, booleans and none/null
                are recognized and returned as proper types instead of strings;
            if `False`, everything is converted to strings
            if `None`, backend return value is used
    Returns:
        parsed `inp` (dict or list) containing unicode values
    Raises:
        various sorts of errors raised by used libraries while parsing
    """
    res = {}

    if fmt == 'ini':
        cfg = configobj.ConfigObj(inp, encoding=encoding)
        res = cfg.dict()
    elif fmt == 'json':
        if six.PY3:
            # python 3 json only reads from unicode objects
            inp = io.TextIOWrapper(inp, encoding=encoding)
        res = json.load(inp, encoding=encoding)
    elif fmt == 'xml':
        res = xmltodict.parse(inp, encoding=encoding)
    elif fmt == 'yaml':
        # guesses encoding by its own, there seems to be no way to pass
        #  it explicitly
        res = yaml.safe_load(inp)
    else:
        raise  # unknown format

    # make sure it's all unicode and all int/float values were parsed correctly
    #   the unicode part is here because of yaml on PY2 and also as workaround for
    #   https://github.com/DiffSK/configobj/issues/18#issuecomment-76391689
    return _ensure_proper_types(res, encoding, force_types)


def _do_serialize(struct, fmt, encoding):
    """Actually serialize input.

    Args:
        struct: structure to serialize to
        fmt: format to serialize to
        encoding: encoding to use while serializing
    Returns:
        encoded serialized structure
    Raises:
        various sorts of errors raised by libraries while serializing
    """
    res = None

    if fmt == 'ini':
        config = configobj.ConfigObj(encoding=encoding)
        for k, v in struct.items():
            config[k] = v
        res = b'\n'.join(config.write())
    elif fmt == 'json':
        # specify separators to get rid of trailing whitespace
        # specify ensure_ascii to make sure unicode is serialized in \x... sequences,
        #  not in \u sequences
        res = json.dumps(struct, indent=2, separators=(',', ': '), ensure_ascii=False).\
                encode(encoding)
    elif fmt == 'xml':
        # passing encoding argument doesn't encode, just sets the xml property
        res = xmltodict.unparse(struct, pretty=True, encoding='utf-8').encode('utf-8')
    elif fmt == 'yaml':
        res = yaml.safe_dump(struct, encoding='utf-8', default_flow_style=False)
    else:
        raise  # unknown format

    return res


def _ensure_proper_types(struct, encoding, force_types):
    """A convenience function that recursively makes sure the given structure
    contains proper types according to value of `force_types`.

    Args:
        struct: a structure to check and fix
        encoding: encoding to use on found bytestrings
        force_types:
            if `True`, integers, floats, booleans and none/null
                are recognized and returned as proper types instead of strings;
            if `False`, everything is converted to strings
            if `None`, unmodified `struct` is returned
    Returns:
        a fully decoded copy of given structure
    """
    if force_types is None:
        return struct

    # if it's an empty value
    res = None
    if isinstance(struct, (dict, collections.OrderedDict)):
        res = type(struct)()
        for k, v in struct.items():
            res[_ensure_proper_types(k, encoding, force_types)] = \
                _ensure_proper_types(v, encoding, force_types)
    elif isinstance(struct, list):
        res = []
        for i in struct:
            res.append(_ensure_proper_types(i, encoding, force_types))
    elif isinstance(struct, six.binary_type):
        res = struct.decode(encoding)
    elif isinstance(struct, (six.text_type, type(None), type(True), six.integer_types, float)):
        res = struct
    else:
        raise AnyMarkupError('internal error - unexpected type {0} in parsed markup'.
            format(type(struct)))

    if force_types and isinstance(res, six.text_type):
        res = _recognize_basic_types(res)
    elif not (force_types or \
            isinstance(res, (dict, collections.OrderedDict, list, six.text_type))):
        res = six.text_type(res)

    return res


def _recognize_basic_types(s):
    """If value of given string `s` is an integer (or long), float or boolean, convert it
    to a proper type and return it.
    """
    tps = [int, float]
    if not six.PY3:  # compat for older versions of six that don't have PY2
        tps.append(long)
    for tp in tps:
        try:
            return tp(s)
        except ValueError:
            pass
    if s.lower() == 'true':
        return True
    if s.lower() == 'false':
        return False
    if s.lower() in ['none', 'null']:
        return None

    return s


def _get_format(format, fname, inp=None):
    """Try to guess markup format of given input.

    Args:
        format: explicit format override to use
        fname: name of file, if a file was used to read `inp`
        inp: optional bytestring to guess format of (can be None, if markup
            format is to be guessed only from `format` and `fname`)
    Returns:
        guessed format (a key of fmt_to_exts dict)
    Raises:
        AnyMarkupError if explicit format override has unsupported value
            or if it's impossible to guess the format
    """
    fmt = None
    err = True

    if format is not None:
        if format in fmt_to_exts:
            fmt = format
            err = False
    elif fname:
        # get file extension without leading dot
        file_ext = os.path.splitext(fname)[1][len(os.path.extsep):]
        for fmt_name, exts in fmt_to_exts.items():
            if file_ext in exts:
                fmt = fmt_name
                err = False

    if fmt is None:
        if inp is not None:
            fmt = _guess_fmt_from_bytes(inp)
            err = False

    if err:
        err_string = 'Failed to guess markup format based on: '
        what = []
        for k, v in {format: 'specified format argument',
                     fname: 'filename', inp: 'input string'}.items():
            if k:
                what.append(v)
        if not what:
            what.append('nothing to guess format from!')
        err_string += ', '.join(what)
        raise AnyMarkupError(err_string)

    return fmt


def _guess_fmt_from_bytes(inp):
    """Try to guess format of given bytestring.

    Args:
        inp: byte string to guess format of
    Returns:
        guessed format
    """
    stripped = inp.strip()
    fmt = None
    ini_section_header_re = re.compile(b'^\[([\w-]+)\]')

    if len(stripped) == 0:
        # this can be anything, so choose json, for example
        fmt = 'yaml'
    else:
        if stripped.startswith(b'<'):
            fmt = 'xml'
        else:
            for l in stripped.splitlines():
                line = l.strip()
                if not line.startswith(b'#') and line:
                    break
            # json, ini or yaml => skip comments and then determine type
            if ini_section_header_re.match(line):
                fmt = 'ini'
            else:
                # we assume that yaml is superset of json
                # TODO: how do we figure out it's not yaml?
                fmt = 'yaml'

    return fmt


# following code makes it possible to use OrderedDict with PyYAML
# based on https://bitbucket.org/xi/pyyaml/issue/13
def construct_ordereddict(loader, node):
    try:
        omap = loader.construct_yaml_omap(node)
        return collections.OrderedDict(*omap)
    except yaml.constructor.ConstructorError:
        return loader.construct_yaml_seq(node)


def represent_ordereddict(dumper, data):
    # NOTE: For block style this uses the compact omap notation, but for flow style
    # it does not.
    values = []
    node = yaml.SequenceNode(u'tag:yaml.org,2002:omap', values, flow_style=False)
    if dumper.alias_key is not None:
        dumper.represented_objects[dumper.alias_key] = node
    for key, value in data.items():
        key_item = dumper.represent_data(key)
        value_item = dumper.represent_data(value)
        node_item = yaml.MappingNode(u'tag:yaml.org,2002:map', [(key_item, value_item)],
                                     flow_style=False)
        values.append(node_item)
    return node


yaml.SafeLoader.add_constructor(u'tag:yaml.org,2002:omap', construct_ordereddict)
yaml.SafeDumper.add_representer(collections.OrderedDict, represent_ordereddict)
