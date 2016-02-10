"""
Functions and objects related to inter-operating-system compatibility.
"""

import os


def get_path_separator():
    """
    Returns the appropriate file path separator depending on operating
    system. That is, when run on UNIX-like systems it returns a forward slash
    ('/'), and for Windows it returns a backslash ('\')
    :return: String. The file path separator for the current operating system.
    """
    if os.name == 'nt':
        return '\\'
    else:
        return '/'
