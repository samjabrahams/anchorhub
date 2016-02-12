"""
Tests for validate_files.py

validate_files.py
http://www.github.com/samjabrahams/anchorhub/validation/validate_files.py
"""
from nose.tools import *

import anchorhub.validation.validate_files as v
from anchorhub.exceptions.validationexception import ValidationException


def test_is_not_empty_success():
    """
    validate_files.py: Run is_not_empty() with correct inputs
    """
    a = ['/dir/test']
    assert v.is_not_empty(a)


@raises(ValidationException)
def test_is_not_empty_failure():
    """
    validate_files.py: Run is_not_empty() with bad inputs
    :raises ValidationException: always, if test is working
    """
    a = []
    assert v.is_not_empty(a)