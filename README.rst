anymarkup
=========

Parse or serialize any markup. Currently supports ini, json, xml and yaml.
Report bugs and new functionality requests at https://github.com/bkabrda/anymarkup/issues.

Parsing (see below for more examples)::

  import anymarkup
  anymarkup.parse('foo: bar')
  anymarkup.parse_file('foo/bar.ini')

Serializing: coming in next version

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
