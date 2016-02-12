"""
File for utility function that returns AnchorHub's root directory.
"""
import os.path as path
import anchorhub


def get_anchorhub_path():
    """
    Returns the absolute path to the AnchorHub directory. Will be used to run
    tests using folders located within the AnchorHub root.

    :return: String path to AnchorHub directory
    """
    return path.abspath(path.dirname(anchorhub.__file__))
