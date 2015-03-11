# -*- coding: utf-8 -*-

from collections import OrderedDict

example_ini = u"""\
[foo]
bar = ěšč
spam = 1
baz = 1.1
[[blah]]
blahblah = True, text4
nothing = None\
"""


example_json = u"""\
{
  "foo": {
    "bar": "ěšč",
    "spam": 1,
    "baz": 1.1,
    "blah": {
      "blahblah": [
        true,
        "text4"
      ],
      "nothing": null
    }
  }
}"""


example_xml = u"""\
<?xml version="1.0" encoding="utf-8"?>
<foo>
\t<bar>ěšč</bar>
\t<spam>1</spam>
\t<baz>1.1</baz>
\t<blah>
\t\t<blahblah>True</blahblah>
\t\t<blahblah>text4</blahblah>
\t\t<nothing></nothing>
\t</blah>
</foo>"""


example_yaml_map = u"""\
foo:
    bar: ěšč
    spam: 1
    baz: 1.1
    blah:
        blahblah:
        - True
        - text4
        nothing:"""


# for testing OrderedDict parsing/serializing with PyYAML
# TODO: what about "nothing: null"? it's not there for normal map
example_yaml_omap = u"""\
!!omap
- foo: !!omap
  - bar: ěšč
  - spam: 1
  - baz: 1.1
  - blah: !!omap
    - blahblah:
      - True
      - text4
    - nothing: null"""


example_as_ordered_dict = OrderedDict(
    [(u'foo', OrderedDict([
        (u'bar', u'ěšč'),
        (u'spam', 1),
        (u'baz', 1.1),
        (u'blah', OrderedDict([
            (u'blahblah', [True, u'text4']),
            (u'nothing', None)
        ]))
    ]))]
)


example_as_dict = {
    u'foo': {
         u'bar': u'ěšč',
         u'spam': 1,
         u'baz': 1.1,
         u'blah': {
             u'blahblah': [True, u'text4'],
             u'nothing': None
         }
    }
}


# ini loading doesn't yield any ints/floats/NoneTypes/bools, so it's ideal
#  to test our custom convertors; for other types, some of these values
#  are pre-converted by the used parsers
types_ini = u"""
[x]
a=1
b=1.1
c=None
d=True"""


types_json = u"""
{
  "x":
    {
      "a": 1,
      "b": 1.1,
      "c": null,
      "d": true,
    }
}"""


types_yaml = u"""
x:
  a: 1
  b: 1.1
  c: None
  d: True
"""


types_xml = u"""\
<?xml version="1.0" encoding="utf-8"?>
<x>
\t<a>1</a>
\t<b>1.1</b>
\t<c>None</c>
\t<d>True</d>
</x>"""


types_as_struct_with_objects = {
    'x': {
        'a': 1,
        'b': 1.1,
        'c': None,
        'd': True,
    }
}


types_as_struct_with_strings = {
    'x': {
        'a': "1",
        'b': "1.1",
        'c': "None",
        'd': "True",
    }
}
