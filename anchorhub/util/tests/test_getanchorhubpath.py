"""
Tests for getanchorhubpath.py

http://www.github.com/samjabrahams/anchorhub/util/getanchorhubpath.py
"""

import os.path as path
from anchorhub.util.getanchorhubpath import get_anchorhub_path
from anchorhub.compatibility import get_path_separator


def test_get_anchorhub_path_directory():
    """
    getanchorhubpath.py: Make sure directory given is named 'anchorhub'
    """
    path = get_anchorhub_path()
    dir = path[path.rfind(get_path_separator()) + 1:]
    assert dir == 'anchorhub'