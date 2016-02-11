"""
Tests for normalize_opts.py

normalize_opts.py
http://www.github.com/samjabrahams/anchorhub/normalization/normalize_opts.py
"""
import os.path as path

import anchorhub.normalization.normalize_opts as n


def test_abs_path_directories():
    a = {'input': '.', 'output': 'anchorhub-out'}
    n.add_abs_path_directories(a)
    assert 'abs_input' in a
    assert 'abs_output' in a
    assert a['abs_input'] == path.abspath('.')
    assert a['abs_output'] == path.abspath('anchorhub-out')