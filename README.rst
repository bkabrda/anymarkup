anymarkup
=========

.. image:: https://travis-ci.org/bkabrda/anymarkup.svg?branch=master
   :target: https://travis-ci.org/bkabrda/anymarkup
   :alt: Build Status

.. image:: https://landscape.io/github/bkabrda/anymarkup/master/landscape.svg?style=flat
   :target: https://landscape.io/github/bkabrda/anymarkup/master
   :alt: Code Health

.. image:: https://coveralls.io/repos/bkabrda/anymarkup/badge.svg?branch=master
   :target: https://coveralls.io/r/bkabrda/anymarkup?branch=master
   :alt: Coverage

Parse or serialize any markup. Currently supports ini, json, xml and yaml.
Report bugs and new functionality requests at https://github.com/bkabrda/anymarkup/issues.

Parsing::

  >>> import anymarkup
  >>> anymarkup.parse('foo: bar')
  {'foo': 'bar'}
  >>> anymarkup.parse_file('foo/bar.ini')
  {'section': {'subsection': {'opt2': 'bar'}, 'opt1': 'foo'}}

  $ cat foo/bar.ini
  [section]
  opt1=foo
  [[subsection]]
  opt2=bar

Serializing::

  >>> import anymarkup
  >>> anymarkup.serialize({'foo': 'bar'}, 'json')
  b'{\n  "foo": "bar"\n}'
  >>> anymarkup.serialize_file({'foo': 'bar'}, 'foo/bar.json')

  $ cat foo/bar.json
  {
    "foo": "bar"
  }

``anymarkup`` is licensed under BSD license. You can download official releases
from https://pypi.python.org/pypi/anymarkup or install them via ``pip install anymarkup``.

``anymarkup`` works with Python 2.7 and >= 3.3.

Notes on Parsing Basic Types
----------------------------

When parsing, ``anymarkup`` recognizes basic types - ``NoneType``, ``int``, ``float`` and ``bool``
(and ``long`` on Python 2) and converts all values to these types. If you want to get
everything as strings, just use ``force_types=False`` with ``parse`` or ``parse_file``. Finally,
you can also use ``force_types=None`` to get whatever the parsing backend returned::

  >>> anymarkup.parse('a: 1')
  {'a': 1}
  >>> anymarkup.parse('a: 1', force_types=False)
  {'a': '1'}
  >>> anymarkup.parse('a: 1', force_types=None)
  {'a': 1}


Backends
--------

``anymarkup`` uses:

- https://pypi.python.org/pypi/configobj/ for ``ini`` parsing
- https://docs.python.org/library/json.html for ``json`` parsing
- https://pypi.python.org/pypi/xmltodict for ``xml`` parsing
- https://pypi.python.org/pypi/PyYAML for ``yaml`` parsing

Notes on OrderedDict
--------------------

Parsing certain types of markup can yield Python's ``OrderedDict`` type - namely
XML documents and YAML ``!!omap`` (see http://yaml.org/type/omap.html). ``anymarkup``
handles this without a problem, but note that if you serialize these as JSON or INI
and then parse again, you'll lose the ordering information (meaning you'll get just
``dict`` back).

This is because JSON and INI parsers (to my knowledge) don't consider
ordering key-value structures important and there's no direct means in these
markup languages to express ordering key-value structures.


Examples
--------

Parsing examples::

  ini = """
  [a]
  foo = bar"""

  json = """
  {"a": {
      "foo": "bar"
  }}"""

  xml = """<?xml version="1.0" encoding="UTF-8"?>
  <a>
      <foo>bar</foo>
  </a>"""

  yaml = """
  a:
    foo: bar
  """

  # these will all yield the same value (except that xml parsing will yield OrderedDict)
  anymarkup.parse(ini)
  anymarkup.parse(json)
  anymarkup.parse(xml)
  anymarkup.parse(yaml)

  # explicitly specify a type of format to expect and/or encoding (utf-8 is default)
  anymarkup.parse('foo: bar', format='yaml', encoding='ascii')

  # by default, anymarkup recognizes basic types (None, booleans, ints and floats)
  #   if you want to get everything as strings, just use force_types=False

  # will yield {'a': 1, 'b': True, 'c': None}
  anymarkup.parse('a: 1\nb: True\nc: None')
  # will yield {'a': '1', 'b': 'True', 'c': 'None'}
  anymarkup.parse('a: 1\nb: True\nc: None', force_types=False)

  # or parse a file
  anymarkup.parse_file('foo.ini')

  # if a file doesn't have a format extension, pass it explicitly
  anymarkup.parse_file('foo', format='json')

  # you can also pass encoding explicitly (utf-8 is default)
  anymarkup.parse_file('bar', format='xml', encoding='ascii')


Serializing examples::

  struct = {'a': ['b', 'c']}

  for fmt in ['ini', 'json', 'xml', 'yaml']:
      # any of the above formats can be used for serializing
      anymarkup.serialize(struct, fmt)

  # explicitly specify encoding (utf-8 is default)
  anymarkup.serialize(struct, 'json', encoding='utf-8')

  # or serialize directly to a file
  anymarkup.serialize_file(struct, 'foo/bar.ini')

  # if a file doesn't have a format extension, pass it explicitly
  anymarkup.serialize_file(struct, 'foo/bar', format='json')

  # you can also pass encoding explicitly (utf-8 is default)
  anymarkup.serialize_file(struct, 'foo/bar', format='json', encoding='ascii')
