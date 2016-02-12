"""
File for strip_prefix_from_list() function
"""


def strip_prefix_from_list(list, strip):
    """
    Goes through a list of strings and removes the specified prefix from the
    beginning of each string in place.

    :param list: a list of strings to be modified in place
    :param strip: a string specifying the prefix to remove from the list
    """
    import re
    strip_esc = re.escape(strip)
    for i in range(len(list)):
        if re.match(strip_esc, list[i]):
            list[i] = list[i][len(strip):]
    del re