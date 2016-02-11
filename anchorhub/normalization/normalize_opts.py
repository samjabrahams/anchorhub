"""
normalize_opts.py - Functions to prepare command line arguments for
validation and use.
"""
import os.path as path

from anchorhub.lib.bunch import Bunch


def normalize(opts):
    """
    Performs various normalization functions on opts, the provided namespace. It
    is assumed that opts has already been validated with
    anchorhub.validation_opts.validate().

    :param opts: a namespace containing options for AnchorHub
    :return: a namespace with the attributes modified
    """
    opts_dict = vars(opts)
    add_abs_path_directories(opts_dict)
    add_open_close_wrappers(opts_dict)
    return Bunch(opts_dict)


def add_abs_path_directories(opts_dict):
    """
    Adds 'abs_input' and 'abs_output' to opts_dict

    :param opts_dict: dictionary that will be modified
    """
    assert 'input' in opts_dict and 'output' in opts_dict
    opts_dict['abs_input'] = path.abspath(opts_dict['input'])
    opts_dict['abs_output'] = path.abspath(opts_dict['output'])


def add_open_close_wrappers(opts_dict):
    """
    Adds 'open' and 'close' to opts_dict. 'open' indicates the opening
    portion of the anchor-indicating wrapper, and 'close' is the closing
    portion.

    :param opts_dict: dictionary that will be modified
    """
    assert 'wrapper' in opts_dict
    opts_dict['open'], opts_dict['close'] = opts_dict['wrapper'].split()




