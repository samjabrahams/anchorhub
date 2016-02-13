"""
Tests for filetolist.py

filetolist.py:
http://www.github.com/samjabrahams/anchorhub/lib/filetolist.py
"""
from anchorhub.lib.filetolist import FileToList
from anchorhub.util.getanchorhubpath import get_anchorhub_path
from anchorhub.compatibility import get_path_separator


def test_file_to_list_basic():
    sep = get_path_separator()
    path = get_anchorhub_path() + sep + 'lib' + sep + 'tests' + sep + \
           'test_data' + sep + 'filelist'
    assert FileToList.to_list(path) == ['Hello!\n', 'My name\n', 'is\n',
                                        'AnchorHub']
