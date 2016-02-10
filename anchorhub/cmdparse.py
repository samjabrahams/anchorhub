"""
cmdparse.py - Functions for command-line argument extracting and parsing
"""

# Global modules
import argparse
import sys
import os
from os import path

import anchorhub as ah
import anchorhub.settings.default_settings as ds


def parse_args(args=None):
    """
    Parse arguments provided as a list of strings, and return a namespace
    with parameter names matching the arguments

    :param args: List of strings to be parsed as command-line arguments. If
        none, reads in sys.argv as the values.
    :return: a namespace containing arguments values
    """
    if args is None:
        args = sys.argv
    parser = argparse.ArgumentParser(description=ds.ARGPARSER['description'])
    parser.add_argument('input', help=ds.ARGPARSE_INPUT['help'])
    parser.add_argument('output', nargs='?', help=ds.ARGPARSE_OUTPUT['help'],
                        default=ds.ARGPARSE_OUTPUT['default'])
    parser.add_argument('-X', '--overwrite', help=ds.ARGPARSE_OVERWRITE['help'],
                        action='store_true')
    parser.add_argument('-e', '--extension', nargs='+', default=['.md'],
                        help=ds.ARGPARSE_EXTENSION['help'])
    parser.add_argument('-w', '--wrapper', help=ds.ARGPARSE_WRAPPER['help'],
                        default=ds.ARGPARSE_WRAPPER['default'], )
    parser.add_argument('-v', '--version', action='version',
                        version=ah.__version__)

    return parser.parse_args(args)


def parse_args_dict(args=None):
    """
    Parse arguments provided as a list of strings, and return a dictionary
    mapping options/flags to provided values
    :param args: List of strings to be parsed as command-line arguments. If
        none, reads in sys.argv as the values.
    :return: a dictionary containing the flags and values as a key/value pair
    """
    return vars(parse_args(args))
