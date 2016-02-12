"""
normalize_opts.py - Functions to prepare command line arguments for
validation and use.
"""
import os.path as path

from anchorhub.lib.bunch import Bunch
from anchorhub.util.addsuffix import add_suffix
from anchorhub.compatibility import get_path_separator


def normalize(opts):
    """
    Performs various normalization functions on opts, the provided namespace. It
    is assumed that opts has already been validated with
    anchorhub.validation_opts.validate().

    :param opts: a namespace containing options for AnchorHub
    :return: a namespace with the attributes modified
    """
    opts_dict = vars(opts)
    ensure_directories_end_in_separator(opts_dict)
    add_abs_path_directories(opts_dict)
    add_open_close_wrappers(opts_dict)
    return Bunch(opts_dict)


def add_abs_path_directories(opts_dict):
    """
    Adds 'abs_input' and 'abs_output' to opts_dict

    :param opts_dict: dictionary that will be modified
    """
    assert_has_input_output(opts_dict)
    opts_dict['abs_input'] = path.abspath(opts_dict['input']) + \
        get_path_separator()
    opts_dict['abs_output'] = path.abspath(opts_dict['output']) + \
        get_path_separator()


def add_open_close_wrappers(opts_dict):
    """
    Adds 'open' and 'close' to opts_dict. 'open' indicates the opening
    portion of the anchor-indicating wrapper, and 'close' is the closing
    portion.

    :param opts_dict: dictionary that will be modified
    """
    assert 'wrapper' in opts_dict
    opts_dict['open'], opts_dict['close'] = opts_dict['wrapper'].split()


def ensure_directories_end_in_separator(opts_dict):
    """
    Adds a path separator to the end of the input and output directories,
    if they don't already have them.

    :param opts_dict: dictionary that will be modified
    """
    assert_has_input_output(opts_dict)
    opts_dict['input'] = add_suffix(opts_dict['input'], get_path_separator())
    opts_dict['output'] = add_suffix(opts_dict['output'], get_path_separator())

def assert_has_input_output(opts_dict):
    """
    Helper that asserts that 'input' and 'output' are keys in the dictionary

    :param opts_dict: dictionary to test
    """
    assert 'input' in opts_dict
    assert 'output' in opts_dict
