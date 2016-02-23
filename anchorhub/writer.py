"""
Class file for the AnchorHub Writer
"""
import os
import os.path
import sys
from abc import ABCMeta, abstractmethod

from anchorhub.lib.filetolist import FileToList
from anchorhub.util.stripprefix import strip_prefix


class Writer(object):
    """
    The Writer class coordinates the parsing and writing of files according
    to the settings specified in its initializer. Its primary client-facing
    method is its write() function, which takes in a list of file_paths,
    a dictionary of AnchorHub tag to anchor key-value pairs.
    """
    def __init__(self, strategies, switches=None):
        """
        The initializer for the Collector.

        :param strategies: Concrete WriterStrategies
        :param switches:
        """
        self._strategies = strategies  # List of concrete WriterStrategy objs
        self._switches = switches  # List of ArmedTestSwitch objects
        self._counter = []
        for s in self._strategies:
            self._counter.append([0, s.get_label()])

    def write(self, file_paths, anchors, opts):
        """

        :param file_paths:
        :param anchors:
        :param opts:
        :return: A list of numbers, counting the number of times each
            strategy was used
        """
        for file_path in file_paths:
            self.write_single_file(file_path, anchors, opts)
            self._reset_switches()
        return self._counter

    def write_single_file(self, file_path, anchors, opts):
        """

        :param file_path:
        :param anchors:
        :param opts:
        :return: A list of numbers, counting the number of times each
            strategy was used
        """
        lines = FileToList.to_list(file_path)
        new_text = []
        file_is_modified = False  # Will only rewrite file when True
        for i in range(len(lines)):
            modified_line = lines[i]
            # Flip any switches that are triggered by this line
            self._try_switches(lines, i)
            if self._no_switches_on():
                for n, s in enumerate(self._strategies):
                    if s.test(modified_line, lines, i):
                        # Strategy detected that it may modify this line
                        mod = s.modify(modified_line, anchors, file_path)
                        if modified_line != mod:
                            # Strategy modified the line
                            modified_line = mod
                            self._counter[n][0] += 1  # Strategy counter +1
                            file_is_modified = True  # Must rewrite this file
            new_text.append(modified_line)
            self._arm_switches()
        if file_is_modified:
            self._write_with_opts(file_path, new_text, opts)
        return self._counter

    def _write_with_opts(self, file_path, lines, opts):
        """

        :param file_path:
        :param lines:
        :param opts
        """
        if opts.overwrite:
            self._write_file_with_list(file_path, lines)
        else:
            if opts.is_dir:
                # Directory style output
                write_path = opts.abs_output + strip_prefix(file_path,
                                                            opts.abs_input)
            else:
                write_path = opts.abs_output + opts.input  # single file output
            self._create_dirs_if_necessary(write_path)
            self._write_file_with_list(write_path, lines)

    def _write_file_with_list(self, file_path, lines):
        """

        :param file_path:
        :param lines:
        :return:
        """
        f = open(file_path, 'wb')
        for i in range(len(lines)):
            if sys.version_info >= (3,1):
                f.write(bytes(lines[i], "UTF-8"))
            else:
                f.write(lines[i])
        f.close()

    def _create_dirs_if_necessary(self, path):
        """

        :param path:
        :return:
        """
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

    def _try_switches(self, lines, index):
        """
        For each switch in the Writer object, pass a list of string,
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
        Arms all switches the Writer object
        """
        for s in self._switches:
            s.arm()

    def _no_switches_on(self):
        """
        Returns True if no _switches are set to True currently in the
        Writer object.

        :return: True if no _switches are set to True in the Collector object
        """
        return not any(s.is_switched() for s in self._switches)

    def _reset_switches(self):
        """
        Sets all switches in the Writer object to False
        """
        for s in self._switches:
            s.force(False)


class WriterStrategy(object):
    __metaclass__ = ABCMeta

    def __init__(self, opts, label=None):
        """
        Initializes any necessary parameters for the WriterStrategy using
        opts, a namespace containing runtime options for AnchorHub

        :param opts: a namespace containing runtime options for AnchorHub,
            typically created from command-line arguments
        :param label: string label describing what this WriterStrategy
            modifies. For example, a WriterStrategy that modified headers
            might use the label 'headers'
        """
        self._label = label

    @abstractmethod
    def test(self, current_modified_line, file_lines=None, index=None):
        """
        Abstract method. Should return True when the line at file_lines[
        index] is a candidate to be modified with this object's modify() method

        :param current_modified_line:
        :param file_lines: List of strings corresponding to lines in a text file
        :param index: index of file_lines corresponding to the line to be tested
        :return: True if the string at file_lines[index] should be modified
        """
        pass

    @abstractmethod
    def modify(self, current_modified_line, anchors, file_path, file_lines=None,
               index=None):
        """
        Abstract method. Should return a parse a line of text and return the
        same string with any modifications that it has made.

        current_modified_line is the current line in the file being parsed
        _after_ any previous WriterStrategy objects have acted upon it.
        file_lines is a list of strings showing the lines in the original
        file, and may be used as reference if necessary. index points to the
        line currently being parsed in file_lines.

        If no previous WriterStrategy objects have acted upon
        current_modified_line, file_lines[index] == current_modified_line

        :param current_modified_line: String that represents the current line
            after modifications from previous WriterStrategy objects
        :param anchors:
        :param file_path:
        :param file_lines: The original file's lines as a list of strings.
            This should not be modified.
        :param index: The index corresponding to the current line in file_lines
        :return: String of the line after modifications
        """
        pass

    def get_label(self):
        """
        Should return a string label describing what this WriterStrategy
        modifies. Used to print summary statistics at the end.

        :return: string label describing what this WriterStrategy modifies
        """
        return self._label
