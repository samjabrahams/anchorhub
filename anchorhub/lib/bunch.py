"""
bunch.py - The Bunch object as described by Alex Martelli. Used to convert
dictionary objects into namespaces.

About Alex Martelli:
https://wiki.python.org/moin/AlexMartelli

Where Bunch was found:
http://stackoverflow.com/questions/2597278/python-load-variables-in-a-dict-into-namespace
"""


class Bunch(object):
    """
    Bunch - converts dictionaries into namespaces
    """
    def __init__(self, adict):
        self.__dict__.update(adict)

