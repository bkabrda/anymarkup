anymarkup
=========

Parse or serialize any markup. Currently supports ini, json, xml and yaml.
Report bugs and new functionality requests at https://github.com/bkabrda/anymarkup/issues.

Parsing::

  import anymarkup
  anymarkup.parse('foo: bar')
  anymarkup.parse_file('foo/bar.ini')

Serializing::

  import anymarkup
  anymarkup.serialize({'foo': 'bar'}, 'json')
  anymarkup.serialize_file({'foo': 'bar'}, 'path/to/file.json')

``anymarkup`` is licensed under BSD license. You can download official releases
from https://pypi.python.org/pypi/anymarkup or install them via ``pip install anymarkup``.

``anymarkup`` works with Python 2.7 and >= 3.3.

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

  import anymarkup

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

  # or parse a file
  anymarkup.parse_file('foo.ini')

  # if a file doesn't have a format extension, pass it explicitly
  anymarkup.parse_file('foo', format='json')

  # you can also pass encoding explicitly (utf-8 is default)
  anymarkup.parse_file('bar', format='xml', encoding='ascii')


Serializing examples::

  import anymarkup

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
