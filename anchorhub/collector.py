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
        :param strategies: a list of concrete CollectorStrategy objects
        :param switches: a list of ArmedCheckSwitches
        """
        self._converter = converter
        self._strategies = strategies
        self._switches = switches
        self._anchors = {}
        self._duplicate_tags = {}
        self.has_duplicates = False

    def collect(self, file_paths):
        """
        Takes in a list of string file_paths, and parses through them using
        the converter, strategies, and switches defined at object
        initialization.

        It returns two dictionaries- the first maps from
        file_path strings to inner dictionaries, and those inner dictionaries
        map from AnchorHub tag to converted anchors.

        The second dictionary maps file_paths to lists. Each entry on the
        list corresponds to a duplicate tag found in the file. The entries
        are lists with the following information: [tag, line_number,
        previous-anchor-used]

        :param file_paths:
        :return: Two dictionaries. The first maps string file paths to
            dictionaries. These inner dictionaries map AnchorHub tags to
            generated anchors. The second dictionary maps file paths to lists
            containing information about duplicate tags found on each page.
        """
        for file_path in file_paths:
            self._anchors[file_path], d = self.collect_single_file(file_path)
            if len(d) > 0:
                # There were duplicates found in the file
                self._duplicate_tags[file_path] = d
            self._reset_switches()
        return self._anchors, self._duplicate_tags

    def collect_single_file(self, file_path):
        """
        Takes in a list of strings, usually the lines in a text file,
        and collects the AnchorHub tags and auto-generated anchors for the
        file according to the  Collector's converter, strategies, and switches

        :param file_path: string file path of file to examine
        :return: A dictionary mapping AnchorHub tags to auto-generated
            anchors, and a list of containing an entry for each duplicate tag
            found on the page.
        """
        lines = FileToList.to_list(file_path)
        file_anchors = {}
        file_duplicates = []
        for i in range(len(lines)):
            # Flip any switches that are triggered by this line
            self._try_switches(lines, i)
            if self._no_switches_on():
                for s in self._strategies:
                    if s.test(lines, i):
                        # This strategy found an anchor and knows how to parse
                        tag, convert_me = s.get(lines, i)
                        if tag in file_anchors:
                            # Duplicate tag
                            file_duplicates.append((tag, i + 1,
                                                    file_anchors[tag]))
                        else:
                            anchor = self._converter(convert_me, file_anchors)
                            file_anchors[tag] = anchor
            self._arm_switches()
        return file_anchors, file_duplicates

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

    def _reset_switches(self):
        """
        Sets all switches in the Collector object to False
        """
        for s in self._switches:
            s.force(False)


class CollectorStrategy(object):
    __metaclass__ = ABCMeta

    def __init__(self, opts):
        pass

    @abstractmethod
    def test(self, file_lines, index):
        """
        Abstract method. Should return True when there is a defined AnchorHub
        tag on the given line.

        :param file_lines: List of strings corresponding to lines in a text file
        :param index: index of file_lines corresponding to the current line
        :return: True if the string in file_lines[index] points to a
            valid AnchorHub tag
        """
        pass

    @abstractmethod
    def get(self, file_lines, index):
        """
        Abstract method. Extracts the AnchorHub tag from the line, as well as
        the portion of the line that should be converted into an anchor.
        Should return a list of two strings- the first entry being the
        AnchorHub tag specified in the file, and the second entry being the
        portion of the line that should be converted into an anchor.

        :param file_lines: List of strings corresponding to lines in a text file
        :param index: index of file_lines corresponding to the current line
        :return: [tag, string] - tag: the extracted AnchorHub tag. string -
            the portion of the line that should be converted into an anchor
        """
        pass
