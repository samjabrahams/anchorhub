"""
Tests for getfiles.py

getfileslist.py:
http://www.github.com/samjabrahams/anchorhub/util/getfiles.py
"""
import os

import anchorhub.util.getfiles as g


def test_is_dir_inside():
    """
    getfiles.py: Test is_dir_inside()
    """
    assert g.is_dir_inside('/home/fake/beep', ['/home/fake'])
    assert not g.is_dir_inside('/home/somewhere/else', ['home/fake'])
    assert g.is_dir_inside('/home/fake', ['/home/fake'])


# NEED TO FIGURE OUT HOW TO PROPERLY WRITE TESTS FOR THE GLOB MODULE
