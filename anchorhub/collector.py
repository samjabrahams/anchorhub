"""
Class file for the AnchorHub Collector
"""
from abc import ABCMeta, abstractmethod

from anchorhub.lib.filetolist import FileToList


class Collector(object):
    """
    The Collector class coordinates the collection of AnchorHub tags,
    and associates those tags to generated anchors. The primary method is its
    collect() function, which takes in a list of file_paths and collects all
    tag/anchor key-value pairs. It accomplishes this using three types of
    user-defined concrete objects:

    * A converter, which takes in a string input and list of
    existing tag/generated anchor key-value pairs, and outputs a converted
    anchor.
    * An ordered list of collection strategies that take in a list of
    strings, containing each line in a text file, and an index pointing to
    the line currently being examined. The strategy uses that information for
    two methods:
        * test(), which detects whether or not there is a valid AnchorHub tag
        on the line, and outputs a boolean value (True if there is a valid tag)
        * get(), which extracts both the AnchorHub tag, as well as the
        portion of the line that is to be converted into an anchor
    * An ordered list of ArmedCheckSwitches, which detect whether a line
    marks a section of text that should not be parsed and whether a line
    marks the end of such a section.
    """
    def __init__(self, converter, strategies, switches=None):
        """
        The initializer for Collector. Takes in concrete classes in order to
        collect AnchorHub tag/anchor key-value pairs.

        :param converter: function that takes in a string line of text and
        list of existing tag/anchor pairs, and outputs a generated anchor string
        :param strategies: a list of collection strategy objects
        :param switches: a list of ArmedCheckSwitches
        """
        self._converter = converter
        self._strategies = strategies
        self._switches = switches
        self._anchors = {}
        self._duplicate_anchors = {}
        self.has_duplicates = False

    def collect(self, file_paths):
        """
        Client facing method. It takes in a list of string file_paths, and
        :param file_paths:
        :return: Dictionary, mapping file string file paths to dictionaries.
            These inner dictionaries map AnchorHub tags to generated anchors.
        """
        for file_path in file_paths:
            self._anchors[file_path] = self.collect_single_file(file_path)

    def collect_single_file(self, file_path):
        """
        Takes in a list of strings, usually the lines in a text file,
        and collects the AnchorHub tags and auto-generated anchors for the
        file according to the  Collector's converter, strategies, and switches

        :param lines: List of strings.
        :return: A dictionary mapping AnchorHub tags to auto-generated anchors
        """
        lines = FileToList.to_list(file_path)
        file_anchors = {}
        for i in range(len(lines)):
            # Flip any switches that are triggered by this line
            self._try_switches(lines, i)
            if self._no_switches_on():
                for s in self._strategies:
                    if s.test(lines, i):
                        # This strategy found an anchor and knows how to parse
                        tag, convert_me = s.get(lines, i, file_anchors)
                        if tag in file_anchors:
                            # Duplicate tag
                            self._handle_duplicate(file_path, i, tag,
                                                   convert_me, file_anchors)
                        else:
                            anchor = self._converter(convert_me, file_anchors)
                            file_anchors[tag] = anchor
            self._arm_switches()
        return file_anchors

    def _try_switches(self, lines, index):
        """
        For each switch in the Collector object, pass a list of string,
        representing lines of text in a file, and an index to the current
        line to try to flip the switch. A switch will only flip on if the line
        passes its 'test_on' method, and will only flip off if the line
        passes its 'test_off' method.

        :param lines: List of strings, usually the lines in a text file
        :param index: Number index pointing to the current line
        """
        for s in self._switches:
            s.switch(lines, index)

    def _arm_switches(self):
        """
        Arms all switches the Collector object
        """
        for s in self._switches:
            s.arm()

    def _no_switches_on(self):
        """
        Returns True if no _switches are set to True currently in the
        Collector object.

        :return: True if no _switches are set to True in the Collector object
        """
        return not any(s.is_switched() for s in self._switches)

    def _handle_duplicate(self, file_path, index, tag, line, file_anchors):
        """
        Places properly formatted duplicate list into self._duplicate_anchors
        dictionary.

        These lists will be read off after reading all files, and displayed
        to the client as an error message with details on how to fix the
        problems.
        """
        if file_path not in self._duplicate_anchors:
            duplicate_anchors[file_path] = []
        duplicate_anchors[file_path].append([line, index + 1,
                                             file_anchors[tag]])


class CollectorStrategy(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def test(self, file_lines, index):
        """
        Abstract method. Should return True when there is a defined AnchorHub
        tag on the given line.

        :param file_lines: List of string lines in a text file
        :param index: The index in file_lines that points to the current line
            being examined
        :return: True if the string in file_lines at index i points to a
            valid AnchorHub tag
        """
        pass

    @abstractmethod
    def get(self, file_lines, index):
        """
        Abstract method. Extracts the AnchorHub tag from the line, as well as
        the portion of the line that should be converted into an anchor.
        Should return a dictionary key-value pair with the tag as the key and
        the portion that should be converted as the value.

        :param file_lines:
        :param index:
        :return:
        """
        pass
