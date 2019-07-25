# -*- coding: utf-8 -*-


TEST_DATA_INI="""\
[section]
string = foobar
number = 1
boolean = False
float = 2.1
empty = None
"""


TEST_DATA_INI_INTERPOLATION="""\
[section]
string = foobar [%%(test)s]
number = 1
boolean = False
float = 2.1
empty = None
"""


TEST_DATA_JSON = """\
{
  "section": {
    "string": "foobar",
    "number": 1,
    "boolean": false,
    "float": 2.1,
    "empty": null
  }
}
"""

TEST_DATA_JSON5 = """\
{
  section: {
    string: "foobar",
    number: 1,
    boolean: false,
    float: 2.1,
    empty: null,
  },
}
"""

TEST_DATA_TOML = """\
[section]
string = "foobar"
number = 1
boolean = false
float = 2.1
empty = "null"
"""

TEST_DATA_TOML_WITHOUT_EMPTY = """\
[section]
string = "foobar"
number = 1
boolean = false
float = 2.1

"""

TEST_DATA_YAML = """\
section:
  string: foobar
  number: 1
  boolean: false
  float: 2.1
  empty: null
"""

TEST_DATA_YAML_SORTED = """\
section:
  boolean: false
  empty: null
  float: 2.1
  number: 1
  string: foobar"""

TEST_DATA_YAML_FROM_XML = """\
!!omap
- section: !!omap
  - string: foobar
  - number: 1
  - boolean: false
  - float: 2.1
  - empty: null"""

TEST_DATA_XML = """\
<?xml version="1.0" encoding="utf-8"?>
<section>
	<string>foobar</string>
	<number>1</number>
	<boolean>false</boolean>
	<float>2.1</float>
	<empty></empty>
</section>
"""
