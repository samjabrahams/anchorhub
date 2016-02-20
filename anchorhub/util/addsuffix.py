"""
File for helper function add_suffix()
"""


def add_suffix(string, suffix):
    """
    Adds a suffix to a string, if the string does not already have that suffix.

    :param string: the string that should have a suffix added to it
    :param suffix: the suffix to be added to the string
    :return: the string with the suffix added, if it does not already end in
        the suffix. Otherwise, it returns the original string.
    """
    if string[-len(suffix):] != suffix:
        return string + suffix
    else:
        return string
