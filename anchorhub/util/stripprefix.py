"""
File for strip_prefix_from_list() function
"""


def strip_prefix(string, strip):
    """
    Strips a prefix from a string, if the string starts with the prefix.

    :param string: String that should have its prefix removed
    :param strip: Prefix to be removed
    :return: string with the prefix removed if it has the prefix, or else it
        just returns the original string
    """
    import re
    strip_esc = re.escape(strip)
    if re.match(strip_esc, string):
        return string[len(strip):]
    else:
        return string


def strip_prefix_from_list(list, strip):
    """
    Goes through a list of strings and removes the specified prefix from the
    beginning of each string in place.

    :param list: a list of strings to be modified in place
    :param strip: a string specifying the prefix to remove from the list
    """
    for i in range(len(list)):
        list[i] = strip_prefix(list[i], strip)
