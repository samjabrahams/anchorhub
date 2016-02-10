"""
Tests for validate_opts.py

validate_opts.py:
http://www.github.com/samjabrahams/anchorhub/validation/validate_opts.py
"""

from nose.tools import *

import anchorhub.validation.validate_opts as v
from anchorhub.exceptions.validationexception import ValidationException
from anchorhub.compatibility import get_path_separator


class OptObj(object):
    """
    Helper class for testing out validate_opts.validate()
    """
    def __init__(self, input=None, output=None, wrapper=None, extensions=None,
                 overwrite = None):
        if input is not None:
            self.input = input
        if output is not None:
            self.output = output
        if wrapper is not None:
            self.wrapper = wrapper
        if extensions is not None:
            self.extensions = extensions
        if overwrite is not None:
            self.overwrite = overwrite


def test_validate_good():
    """
    validate_opts.py: Test validate() with good inputs
    """

    a = OptObj(input='.', output='anchorhub-out', wrapper='{ }',
               extensions=['.md'], overwrite=False)
    assert v.validate(a)

    b = OptObj(input='.', output='.', wrapper='{ }',
               extensions=['.md'], overwrite=True)
    assert v.validate(b)

    c = OptObj(input='.', output='anchorhub-out', wrapper='[--> ????',
               extensions=['.md'], overwrite=False)
    assert v.validate(c)

    d = OptObj(input='.', output='anchorhub-out', wrapper='{ }',
               extensions=['.md', '.rst', '.hub'], overwrite=False)
    assert v.validate(d)


@raises(ValidationException)
def test_validate_bad_overwrite():
    """
    validate_opts.py: Test validate() with same input/output, overwrite=False
    """
    a = OptObj(input='.', output='.', wrapper='{ }', extensions=['.md'],
               overwrite=False)
    assert v.validate(a)


@raises(ValidationException)
def test_validate_bad_wrapper():
    """
    validate_opts.py: Test validate() with bad wrapper format
    """
    a = OptObj(input='.', output='anchorhub-out', wrapper='{ } { }',
               extensions=['.md'], overwrite=False)
    assert v.validate(a)


@raises(ValidationException)
def test_validate_bad_extensions():
    """
    validate_opts.py: Test validate() with bad extension list
    """
    a = OptObj(input='.', output='anchorhub-out', wrapper='{ }',
               extensions=['.md', '', '.rst'], overwrite=False)
    assert v.validate(a)


@raises(ValueError)
def test_validate_bad_opt():
    """
    validate_opts.py: Test validate() with missing attributes in opts
    """
    a = OptObj(input='.', output='anchorhub-out', wrapper='{ }',
               overwrite=False)
    assert v.validate(a)

