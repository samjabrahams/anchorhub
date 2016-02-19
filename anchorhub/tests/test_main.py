"""
test_main.py - Tests for main.py

main.py:
http://www.github.com/samjabrahams/anchorhub/main.py
"""
from nose.tools import *

import anchorhub.main as main
from anchorhub.util.getanchorhubpath import get_anchorhub_path
from anchorhub.compatibility import get_path_separator


def test_one():
    """
    main.py: Test defaults with local directory as input.
    """
    main.main([get_anchorhub_path() + get_path_separator() +
               '../sample/multi-file', get_anchorhub_path() +
               get_path_separator() + 'tests/anchorhub-out'])
