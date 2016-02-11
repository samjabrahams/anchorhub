"""
Tests for add_suffix.py

add_suffix.py:
http://www.github.com/samjabrahams/anchorhub/normalize_opts.py
"""


from anchorhub.util.addsuffix import add_suffix


def test_add_suffix():
    """
    normalize_ops.py: Test add_suffix()

    add_suffix() should add a suffix to a string, unless that string already
    ends with the suffix.
    """
    a = 'test'
    assert add_suffix(a, 'cow') == 'testcow'

    b = 'this_has_suffix.md'
    assert add_suffix(b, '.md') == b



