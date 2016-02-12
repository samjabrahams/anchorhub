"""
Tests for strip_prefix_from_list()

http://www.github.com/samjabrahams/anchorhub/util/strip_prefix.py
"""

from anchorhub.util.stripprefix import strip_prefix_from_list


def test_strip_prefix_from_list():
    """
    normalize_ops.py: Test strip_prefix_from_list()

    The function should remove the specified prefix from entries that have
    that prefix.
    """
    a = ['./abc', 'def', './../heya']
    strip_prefix_from_list(a, './')
    print(a)
    assert a == ['abc', 'def', '../heya']

    b = ['^[a]$this', '^[a]$should', 'work']
    strip_prefix_from_list(b, '^[a]$')
    assert b == ['this', 'should', 'work']