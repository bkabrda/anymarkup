# -*- coding: utf-8 -*-

from collections import OrderedDict

example_json = u"""\
{
  "foo": {
    "bar": "ěšč",
    "spam": "text2",
    "blah": {
      "blahblah": [
        "text3",
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
\t<spam>text2</spam>
\t<blah>
\t\t<blahblah>text3</blahblah>
\t\t<blahblah>text4</blahblah>
\t\t<nothing></nothing>
\t</blah>
</foo>"""


example_yaml_map = u"""\
foo:
    bar: ěšč
    spam: text2
    blah:
        blahblah:
        - text3
        - text4
        nothing:"""


# for testing OrderedDict parsing/serializing with PyYAML
# TODO: what about "nothing: null"? it's not there for normal map
example_yaml_omap = u"""\
!!omap
- foo: !!omap
  - bar: ěšč
  - spam: text2
  - blah: !!omap
    - blahblah:
      - text3
      - text4
    - nothing: null"""


example_as_ordered_dict = OrderedDict(
    [(u'foo', OrderedDict([
        (u'bar', u'ěšč'),
        (u'spam', u'text2'),
        (u'blah', OrderedDict([
            (u'blahblah', [u'text3', u'text4']),
            (u'nothing', None)
        ]))
    ]))]
)


example_as_dict = {
    u'foo': {
         u'bar': u'ěšč',
         u'spam': u'text2',
         u'blah': {
             u'blahblah': [u'text3', u'text4'],
             u'nothing': None
         }
    }
}


example_ini = u"""\
[foo]
bar = ěšč
spam = text2
[[blah]]
blahblah = text3, text4
nothing = ""\
"""

# there seems to be no way to represent "None" in inifile...
example_ini_as_dict = {
    u'foo': {
         u'bar': u'ěšč',
         u'spam': u'text2',
         u'blah': {
             u'blahblah': [u'text3', u'text4'],
             u'nothing': u''
         }
    }
}
