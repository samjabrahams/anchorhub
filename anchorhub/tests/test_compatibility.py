"""
Tests for compatibility.py

compatibility.py:
http://www.github.com/samjabrahams/anchorhub/compatibility.py
"""

import os

import anchorhub.compatibility as compat


def test_get_path_separator():
    """
    compatibility.py: Test get_path_separator()

    Test to make sure get_path_separator() returns the proper path separator.
    """
    if os.name == 'nt':
        assert compat.get_path_separator() == '\\'
    else:
        assert compat.get_path_separator() == '/'
