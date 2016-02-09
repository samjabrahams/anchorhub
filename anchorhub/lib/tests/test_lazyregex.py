"""
Tests for the LazyRegex class

LazyRegex:
http://www.github.com/samjabrahams/anchorhub/lib/lazyregex.py
"""

import re

from anchorhub.lib.lazyregex import LazyRegex


def test_init():
    """
    Test basic LazyRegex initialization and parameter assignment
    """
    l = LazyRegex("beep")
    assert l.get_pattern() == "beep"


def test_search():
    """
    Test the LazyRegex.search() method
    """
    l = LazyRegex("beep")
    assert l.search("This is a beep sentence.")
    assert l.search("This string should not match.") is None


def test_match():
    """
    Test the LazyRegex.match() method
    """
    l = LazyRegex("beep")
    assert l.match("This shouldn't match! beep beep beep.") is None
    assert l.match("beep this should match")


def test_get_regex():
    """
    Tests LazyRegex.get_regex() method
    """
    l = LazyRegex("beep")
    assert type(l.get_regex()) == type(re.compile("beep"))


def test_laziness():
    """
    Test to make sure LazyRegex doesn't create the compiled regular
    expression object until it is needed.
    """
    l = LazyRegex("beep")
    assert l._regex is None
    assert l.get_regex()
    assert l._regex is not None

def test_get_pattern():
    """
    Test the LazyRegex.get_pattern() method
    """
    l = LazyRegex("beep")
    assert l.get_pattern() == "beep"

