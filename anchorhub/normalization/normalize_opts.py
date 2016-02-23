"""
normalize_opts.py - Functions to prepare command line arguments for
validation and use.
"""
import os.path as path
import re

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
    add_is_dir(opts_dict)
    ensure_directories_end_in_separator(opts_dict)
    add_abs_path_directories(opts_dict)
    add_open_close_wrappers(opts_dict)
    add_wrapper_regex(opts_dict)
    return Bunch(opts_dict)


def add_abs_path_directories(opts_dict):
    """
    Adds 'abs_input' and 'abs_output' to opts_dict

    :param opts_dict: dictionary that will be modified
    """
    assert_has_input_output(opts_dict)
    opts_dict['abs_input'] = path.abspath(opts_dict['input'])
    if opts_dict['is_dir']:
        # Only add path separator to input if it is a directory
        opts_dict['abs_input'] += get_path_separator()
    opts_dict['abs_output'] = path.abspath(opts_dict['output']) + \
        get_path_separator()


def add_open_close_wrappers(opts_dict):
    """
    Adds 'open' and 'close' to opts_dict. 'open' indicates the opening
    portion of the AnchorHub tag-indicating wrapper, and 'close' is the closing
    portion.

    :param opts_dict: dictionary that will be modified
    """
    assert 'wrapper' in opts_dict
    opts_dict['open'], opts_dict['close'] = opts_dict['wrapper'].split()


def add_is_dir(opts_dict):
    """
    Checks to see if the input argument is a directory, and adds the key
    'is_dir' to opts_dict. The value is True if it is a directory,
    and False if it is not.

    :param opts_dict: Dictionary that will be modified
    """
    assert_has_input_output(opts_dict)
    opts_dict['is_dir'] = path.isdir(opts_dict['input'])


def ensure_directories_end_in_separator(opts_dict):
    """
    Adds a path separator to the end of the input and output directories,
    if they don't already have them.

    :param opts_dict: dictionary that will be modified
    """
    assert_has_input_output(opts_dict)
    assert 'is_dir' in opts_dict
    if opts_dict['is_dir']:
        opts_dict['input'] = add_suffix(opts_dict['input'],
                                        get_path_separator())
    opts_dict['output'] = add_suffix(opts_dict['output'], get_path_separator())


def assert_has_input_output(opts_dict):
    """
    Helper that asserts that 'input' and 'output' are keys in the dictionary

    :param opts_dict: dictionary to test
    """
    assert 'input' in opts_dict
    assert 'output' in opts_dict


def add_wrapper_regex(opts_dict):
    """
    Adds the regular expression for the specified wrapper to opts_dict. It
    is assumed the dictionary has the keys 'open' and 'close'

    The regular expression will match the following, in order:

    1. The wrapper 'open' pattern
    2. Followed by any amount of white space (or none)
    3. Followed by a '#' character
    4. Followed by one or more non-whitespace characters, but _not_ matching
    the wrapper 'open' pattern, or the wrapper 'close' pattern
    5. Followed by any amount of white space (or none)
    6. Followed by the wrapper 'close' pattern

    For example, it would match the following string, assuming the default
    curly brace wrapper pattern:
    '{ #tag }'

    But it would _not_ match this:
    '{{ #tag }}'
    :param opts_dict: Dictionary that will be modified.
    """
    opn = re.escape(opts_dict['open'])
    close = re.escape(opts_dict['close'])

    p = opn         # The opening pattern
    p += r"\s*"     # Any amount of white space
    p += r"#"       # Hash '#' sign
    # 1+ non-whitespace characters that don't make the open or close pattern
    p += r"((?!" + opn + r")(?!" + close +")\S)+"
    p += r"\s*"     # Any amount of white space
    p += close      # The closing pattern

    opts_dict['wrapper_regex'] = p
