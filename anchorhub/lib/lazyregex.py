"""
Class file for LazyRegex
"""

import re


class LazyRegex(object):
    """
    LazyRegex is a way to lazily instantiate re module compiled pattern
    objects. It stores the desired pattern as a property, but doesn't create
    the underlying regular expression object until it is needed.

    Python re module:
    https://docs.python.org/3/library/re.html
    https://docs.python.org/2/library/re.html
    """
    def __init__(self, pattern):
        """
        Initializer for LazyRegex. Takes in a pattern and stores it for later
        re.compile() use.

        :param pattern: String. Regular expression pattern to be compiled when
            needed.
        """
        self._pattern = pattern
        self._regex = None

    def search(self, string):
        """
        Helper method that calls the underlying regular expression object's
        search() method. Looks for the first location where the regular
        expression object matches.

        :param string: String. The text to test the regular expression
            against.
        :return: Returns a MatchObject instance if it does find a match,
            otherwise returns None
        """
        self._create_regex_if_none()
        return self._regex.search(string)

    def match(self, string):
        """
        Helper method that calls the underlying regular expression object's
        match() method. Checks to see if the regular expression matches the
        _beginning_ of the string.

        :param string: String. Text to match the regular expression against.
        :return: Returns a MatchObject instance if it does find a match,
            otherwise returns None
        """
        self._create_regex_if_none()
        return self._regex.match(string)

    def get_regex(self):
        """
        Get the underlying compiled regular expression object.

        :return: Compiled regular expression object
        """
        self._create_regex_if_none()
        return self._regex

    def get_pattern(self):
        """
        Get the regular expression string provided at initialization

        :return: String. Regular expression pattern associated with the
            object.
        """
        return self._pattern

    def _create_regex_if_none(self):
        """
        Private function. Checks to see if the local regular expression
        object has been created yet
        """
        if self._regex is None:
            self._regex = re.compile(self._pattern, re.UNICODE)
