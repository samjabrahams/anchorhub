"""
Tests validation functions in validate_extensions.py

validate_extensions.py:
http://www.github.com/samjabrahams/anchorhub/validation/validate_extensions.py
"""

from nose.tools import *

import anchorhub.validation.validate_extensions as v


def test_validate_correct():
    """
    validate_extensions.py: Test validate() on correct lists
    """
    a = ['.ds', '.md', 'eeyy']
    assert v.validate(a)

    b = ['.md']
    assert v.validate(b)

    c = ['t', 't', 't', 't', 't', 't']
    assert v.validate(c)


@raises(ValueError)
def test_validate_incorrect_empty_string():
    """
    validate_extensions.py: Test validate() on lists with empty strings

    :raises ValueError: always, if the test is working
    """
    a = ['.md', '.rst', '']
    assert v.validate(a)


@raises(ValueError)
def test_validate_incorrect_empty_list():
    """
    validate_extensions.py: Test validate() on an empty list

    :raises ValueError: always, if the test is working
    """
    a = []
    assert v.validate(a)


class ExtSpace(object):
    """
    Simple class to test out namespace implementations of validate_extensions()
    """
    def __init__(self, e=None):
        if e is not None:
            self.extensions = e


def test_validate_correct_namespace():
    """
    validate_extensions.py: Test validate() on correct namespaces
    """
    a = ExtSpace(e=['.ds', '.md', 'eeyy'])
    assert v.validate(a)

    b = ExtSpace(e=['.md'])
    assert v.validate(b)

    c = ExtSpace(e=['t', 't', 't', 't', 't', 't'])
    assert v.validate(c)


@raises(ValueError)
def test_validate_empty_string_namespace():
    """
    validate_extensions.py: Test validate() on a namespace with an empty string

    Try validatign a namespace that has an empty string as part of the list
    under its extensions attribute.

    :raises ValueError: always, if the test is working
    """
    a = ExtSpace(e=['.md', '.rst', ''])
    assert v.validate(a)


@raises(ValueError)
def test_validate_empty_array_namespace():
    """
    validate_extensions.py: Test validate() on a namespace with empty array

    :raises ValueError: always, if the test is working
    """
    a = ExtSpace(e=['.md', '.rst', ''])
    assert v.validate(a)