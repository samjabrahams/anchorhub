"""
test_main.py - Tests for main.py

main.py:
http://www.github.com/samjabrahams/anchorhub/main.py
"""
from nose.tools import *

import anchorhub.main as main


def test_one():
    """
    main.py: Test defaults with local directory as input.
    """
    main.main(['.'])
