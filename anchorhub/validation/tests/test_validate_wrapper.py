"""
Tests validation functions in validate_wrappers.py

http://www.github.com/samjabrahams/anchorhub/validation/validate_wrappers.py
"""
from nose.tools import *

import anchorhub.validation.validate_wrapper as v
from anchorhub.exceptions.validationexception import ValidationException


class WrapSpace(object):
    """
    Simple class to test out namespace implementations of validate_extensions()
    """
    def __init__(self, w=None):
        if w is not None:
            self.wrapper = w


def test_validate_correct():
    """
    validate_wrapper.py: Test validate() on correct wrapper strings
    """
    a = "{ }"
    assert v.validate(a)

    b = "[-->       <--]"
    assert v.validate(b)

    c = "$$$$ $$$$"
    assert v.validate(c)


@raises(ValidationException)
def test_validate_incorrect_empty_string():
    """
    validate_wrapper.py: Test validate() with an empty string

    :raises ValidationException: always, if the test is working
    """
    assert v.validate("")


@raises(ValidationException)
def test_validate_incorrect_too_many_strings():
    """
    validate_wrapper.py: Test validate() using a string with too many 'words'

    :raises ValidationException: always, if the test is working
    """
    assert v.validate("TOO MANY WORDS")


def test_validate_correct_namespace():
    """
    validate_wrapper.py: Test validate() on a correct namespace object
    """
    a = WrapSpace(w="{ }")
    assert v.validate(a)

    b = WrapSpace(w="[-->       <--]")
    assert v.validate(b)

    c = WrapSpace(w="$$$$ $$$$")
    assert v.validate(c)


@raises(ValidationException)
def test_validate_incorrect_empty_string_namespace():
    """
    validate_wrapper.py: Test validate() on a namespace with an empty string

    :raises ValidationException: always, if the test is working
    """
    a = WrapSpace(w="")
    assert v.validate(a)


@raises(ValidationException)
def test_validate_incorrect_too_many_strings_namespace():
    """
    validate_wrapper.py: Test validate() on a namespace with too many 'words'

    :raises ValidationException: always, if the test is working
    """
    a = WrapSpace(w="TOO MANY WORDS")
    assert v.validate(a)


@raises(ValueError)
def test_validate_wrapper_attr_not_string():
    """
    validate_wrapper.py: Test validate() on namespace with non-string 'wrapper'

    :raises ValueError: always, if the test is working
    """
    a = WrapSpace(w=3)
    assert v.validate(a)


@raises(ValueError)
def test_validate_no_wrapper_attr():
    """
    validate_wrapper.py: Test validate() with an object lacking attr 'wrapper'

    :raises ValueError: always, if the test is working
    """
    assert v.validate(object())