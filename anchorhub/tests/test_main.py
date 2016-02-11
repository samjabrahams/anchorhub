"""
test_main.py - Tests for main.py

main.py:
http://www.github.com/samjabrahams/anchorhub/main.py
"""

import anchorhub.main as main


def test_one():
    """
    main.py: Test defaults with local directory as input.
    """
    main.main(['.'])
