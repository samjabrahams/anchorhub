"""
Tests for hasattrs.py

hasattrs.py:
http://www.github.com/samjabrahams/anchorhub/util/hasattrs.py
"""
from anchorhub.util.hasattrs import hasattrs


class AttrObj(object):
    """
    Basic class with dummy attributes used to test hasattrs()
    """
    def __init__(self):
        self.a = 'a'
        self.b = 'b'
        self.c = 'c'

    def d(self):
        pass


def test_hasattrs_basic():
    """
    hasattrs.py: Basic usage
    """
    a = AttrObj()
    assert hasattrs(a, 'a', 'b', 'c')
    assert hasattrs(a, 'a')
    assert hasattrs(a, 'b', 'd')
    assert not hasattrs(a, 'e')


def test_hasattrs_no_names():
    """
    hasattrs.py: Provide no attribute names
    """
    a = AttrObj()
    assert hasattrs(a)