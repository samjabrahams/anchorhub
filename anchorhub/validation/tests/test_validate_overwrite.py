"""
Tests for validate_overwrite.py

validate_overwrite.py:
http://www.github.com/samjabrahams/anchorhub/validation/validate_overwrite.py
"""
import os

from nose.tools import *

import anchorhub.validation.validate_overwrite as v
from anchorhub.exceptions.validationexception import ValidationException
from anchorhub.compatibility import get_path_separator


class OverObj(object):
    """
    Dummy class for testing overwrite
    """
    def __init__(self, input=None, output=None, overwrite=None):
        if input is not None:
            self.input = input
        if output is not None:
            self.output = output
        if overwrite is not None:
            self.overwrite = overwrite


def test_validate_correct():
    """
    validate_overwrite.py: Test various correct objects
    """
    a = OverObj('.', 'anchorhub-out', False)
    assert v.validate(a)

    b = OverObj('.', '.', True)
    assert v.validate(b)

    c = OverObj('.', 'anchorhub-out', True)
    assert v.validate(c)


@raises(ValidationException)
def test_validate_same_input_output():
    """
    validate_overwrite.py: input/output are the same, overwrite set to False
    """
    a = OverObj('.', '.', False)
    assert v.validate(a)


@raises(ValidationException)
def test_validate_same_input_output_relative_abs_dirs():
    """
    validate_overwrite.py: input/output are same, mixing relative/absolute paths
    """
    cwd = os.getcwd()
    a = OverObj('.', cwd, False)
    assert v.validate(a)


@raises(ValidationException)
def test_validate_same_input_output_relative_dirs():
    """
    validate_overwrite.py: input/output are same, using only relative paths
    """
    cwd = os.getcwd()
    # Find last path separator in cwd; dir is everything after that
    dir = cwd[cwd.rfind(get_path_separator()):]
    a = OverObj('.', '..' + dir, False)
    assert v.validate(a)


@raises(ValueError)
def test_validate_no_input():
    """
    validate_overwrite.py: no input provided
    """
    a = OverObj(output='.', overwrite=False)
    assert v.validate(a)


@raises(ValueError)
def test_validate_no_output():
    """
    validate_overwrite.py: no output provided
    """
    a = OverObj(input='.', overwrite=False)
    assert v.validate(a)


@raises(ValueError)
def test_validate_no_overwrite():
    """
    validate_overwrite.py: no overwrite flag provided
    """
    a = OverObj(input='.', output='.')
    assert v.validate(a)

