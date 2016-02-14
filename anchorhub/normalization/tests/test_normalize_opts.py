"""
Tests for normalize_opts.py

normalize_opts.py
http://www.github.com/samjabrahams/anchorhub/normalization/normalize_opts.py
"""
import os.path as path

import anchorhub.normalization.normalize_opts as n
from anchorhub.compatibility import get_path_separator


class NormObj(object):
    """
    Helper class for testing out normalize_opts.normalize()
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

def test_normalize():
    """
    normalize_opts.py: Test normalize()
    """
    a = NormObj('.', 'anchorhub-out', '{ }', ['.md'], False)
    a = n.normalize(a)
    assert a.input == '.' + get_path_separator()
    assert a.output == 'anchorhub-out' + get_path_separator()
    assert a.open == '{'
    assert a.close == '}'
    assert a.abs_input == path.abspath(a.input) + get_path_separator()
    assert a.abs_output == path.abspath(a.output) + get_path_separator()


def test_abs_path_directories():
    """
    normalize_opts.py: Test add_abs_path_directories()
    """
    a = {'input': '.',
         'output': 'anchorhub-out'}
    n.add_abs_path_directories(a)
    assert 'abs_input' in a
    assert 'abs_output' in a
    assert a['abs_input'] == path.abspath('.') + get_path_separator()
    assert a['abs_output'] == path.abspath('anchorhub-out')+get_path_separator()


def test_add_open_close_wrapper():
    """
    normalize_opts.py: Test add_open_close_wrapper()
    """
    a = {'wrapper': '[--> <--]'}
    n.add_open_close_wrappers(a)
    assert 'open' in a
    assert 'close' in a
    assert a['open'] == '[-->'
    assert a['close'] == '<--]'


def test_ensure_directories_end_in_separator():
    """
    normalize_opts.py: Test ensure_directories_end_in_separator()
    """
    a = {'input': '.', 'output': 'anchorhub-out'}
    n.ensure_directories_end_in_separator(a)
    assert a['input'] == '.' + get_path_separator()
    assert a['output'] == 'anchorhub-out' + get_path_separator()

    b = {'input': 'hello' + get_path_separator(),
         'output': 'dolly' + get_path_separator()}
    n.ensure_directories_end_in_separator(b)
    assert b['input'] == 'hello' + get_path_separator()
    assert b['output'] == 'dolly' + get_path_separator()


def test_add_wrapper_regex():
    """
    normalize_opts.py: Test add_wrapper_regex()
    """
    a = {'open': '{', 'close': '}'}
    n.add_wrapper_regex(a)
    assert 'wrapper_regex' in a
    assert a['wrapper_regex'] == r"\{\s*#((?!\{)(?!\})\S)+\s*\}"
