# -*- coding: utf-8 -*-
import io
import json
import os
import re

import configobj
import six
import xmltodict
import yaml


__all__ = ['AnyMarkupError', 'parse', 'parse_file']
__version__ = '0.1.1'


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


def parse(inp, format=None, encoding='utf-8'):
    """Parse input from file-like object, unicode string or byte string.

    Args:
        inp: file-like object, unicode string or byte string with the markup
        format: explicitly override the guessed `inp` markup format
        encoding: `inp` encoding, defaults to utf-8
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
    fmt = _get_format(proper_inp, format, fname)

    # make it look like file-like bytes-yielding object
    proper_inp = six.BytesIO(proper_inp)

    try:
        res = _do_parse(proper_inp, fmt, encoding)
    except Exception as e:
        # I wish there was only Python 3 and I could just use "raise ... from e"
        raise AnyMarkupError(e)
    if res is None:
        res = {}

    return res


def parse_file(path, format=None, encoding='utf-8'):
    """A convenience wrapper of parse, which accepts path of file to parse.

    Args:
        path: path to file to parse
        format: explicitly override the guessed `inp` markup format
        encoding: file encoding, defaults to utf-8
    Returns:
        parsed `inp` (dict or list) containing unicode values
    Raises:
        AnyMarkupError if a problem occurs while parsing
    """
    try:
        return parse(open(path, 'rb'), format, encoding)
    except EnvironmentError as e:
        raise AnyMarkupError(e)


def _do_parse(inp, fmt, encoding):
    """Actually parse input.

    Args:
        inp: bytes yielding file-like object
        fmt: format to use for parsing
        encoding: encoding of `inp`
    Returns:
        parsed `inp` (dict or list) containing unicode values
    Raises:
        various sorts of errors raised by used libraries while parsing
    """
    res = {}

    if fmt == 'ini':
        cfg = configobj.ConfigObj(inp, encoding=encoding)
        # workaround https://github.com/DiffSK/configobj/issues/18#issuecomment-76391689
        res = cfg.dict()
        if six.PY2:
            res = _ensure_unicode_recursive(res, encoding)
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
        res = yaml.load(inp)
        if six.PY2:
            res = _ensure_unicode_recursive(res, encoding)
    else:
        raise  # unknown format

    return res


def _ensure_unicode_recursive(struct, encoding):
    """A convenience function that recursively makes sure all the strings
    in the structure are decoded unicode. It decodes them if not.

    Args:
        struct: a structure to check and fix
        encoding: encoding to use on found bytestrings
    Returns:
        a fully decoded copy of given structure
    """
    # if it's an empty value
    res = None
    if isinstance(struct, dict):
        res = {}
        for k, v in struct.items():
            res[_ensure_unicode_recursive(k, encoding)] = \
                _ensure_unicode_recursive(v, encoding)
    elif isinstance(struct, list):
        res = []
        for i in struct:
            res.append(_ensure_unicode_recursive(i, encoding))
    elif isinstance(struct, six.binary_type):
        res = struct.decode(encoding)
    elif isinstance(struct, (six.text_type, type(None), type(True))):
        res = struct
    else:
        raise AnyMarkupError('internal error - unexpected type {0} in parsed markup'.
            format(type(struct)))

    return res


def _get_format(inp, format, fname):
    """Try to guess markup format of given input.

    Args:
        inp: bytestring to guess format of
        format: explicit format override to use
        fname: name of file, if a file was used to read `inp`
    Returns:
        guessed format (a key of fmt_to_exts dict)
    Raises:
        AnyMarkupError if explicit format override has unsupported value
            or if it's impossible to guess the format
    """
    fmt = None
    err = None

    if format is not None:
        if format in fmt_to_exts:
            fmt = format
        else:
            err = 'unknown format "{0}"'.format(format)
    elif fname:
        # get file extension without leading dot
        file_ext = os.path.splitext(fname)[1][len(os.path.extsep):]
        for fmt_name, exts in fmt_to_exts.items():
            if file_ext in exts:
                fmt = fmt_name
    if fmt is None:
        fmt = _guess_fmt_from_bytes(inp)
        if fmt is None: 
            err = 'failed to guess markup type from string'

    if err is not None:
        raise AnyMarkupError(err)

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
