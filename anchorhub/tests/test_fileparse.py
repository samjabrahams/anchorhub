"""
Tests for fileparse.py

fileparse.py:
http://www.github.com/samjabrahams/anchorhub/anchorhub/fileparse.py
"""
import os.path

from anchorhub.fileparse import get_file_list
from anchorhub.util.getanchorhubpath import get_anchorhub_path
from anchorhub.compatibility import get_path_separator

sep = get_path_separator()

class FileObj(object):
    """
    Helper class for testing out fileparse.get_file_list
    """
    def __init__(self, abs_input=None, abs_output=None, extensions=None,
                 recursive=None, is_dir=None, input=None):
        if abs_input is not None:
            self.abs_input = abs_input
        if abs_output is not None:
            self.abs_output = abs_output
        if extensions is not None:
            self.extensions = extensions
        if recursive is not None:
            self.recursive = recursive
        if is_dir is not None:
            self.is_dir = is_dir
        if input is not None:
            self.input = input


def test_get_file_list_dir():
    # path to this file's directory
    d = get_anchorhub_path() + sep + 'tests' + sep

    abs_input = d + 'test_data' + sep
    abs_output = d + 'anchorhub-out' + sep
    extensions = ['.md', '.markdown']
    recursive = False
    is_dir = True

    a = FileObj(abs_input=abs_input, abs_output=abs_output,
                extensions=extensions, recursive=recursive, is_dir=is_dir)
    l = get_file_list(a)

    expected_files = [
        d + 'test_data' + sep + 'file1.md',
        d + 'test_data' + sep + 'file2.markdown'
    ]

    assert len(l) == len(expected_files)
    for f in expected_files:
        assert f in l


def test_get_file_list_dir_recursive():
    # path to this file's directory
    d = get_anchorhub_path() + sep + 'tests' + sep

    abs_input = d + 'test_data' + sep
    abs_output = d + 'anchorhub-out' + sep
    extensions = ['.md', '.markdown']
    recursive = True
    is_dir = True

    a = FileObj(abs_input=abs_input, abs_output=abs_output,
                extensions=extensions, recursive=recursive, is_dir=is_dir)
    l = get_file_list(a)

    expected_files = [
        d + 'test_data' + sep + 'file1.md',
        d + 'test_data' + sep + 'file2.markdown',
        d + 'test_data' + sep + 'dir' + sep + 'file4.md',
        d + 'test_data' + sep + 'dir' + sep + 'file5.markdown'
    ]

    assert len(l) == len(expected_files)
    for f in expected_files:
        assert f in l


def test_get_file_list_single():
    # path to this file's directory
    d = get_anchorhub_path() + sep + 'tests' + sep

    abs_input = d + 'test_data' + sep + 'file2.markdown'
    abs_output = d + 'anchorhub-out' + sep
    extensions = ['.md', '.markdown']
    recursive = False
    is_dir = False

    a = FileObj(input=abs_input, abs_input=abs_input, abs_output=abs_output,
                extensions=extensions, recursive=recursive, is_dir=is_dir)
    l = get_file_list(a)

    expected_files = [
        d + 'test_data' + sep + 'file2.markdown'
    ]

    assert len(l) == len(expected_files)
    for f in expected_files:
        assert f in l

