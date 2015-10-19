import anymarkup, anymarkup_core

def test_imports():
    for i in ['AnyMarkupError', 'parse', 'parse_file', 'serialize', 'serialize_file']:
        assert getattr(anymarkup, i) is getattr(anymarkup_core, i)
