"""
Concrete CollectorStrategy classes for the GitHub built-in module
"""
import re

from anchorhub.collector import CollectorStrategy
import anchorhub.builtin.regex.markdown as mdrx


class MarkdownATXCollectorStrategy(CollectorStrategy):
    """
    Concrete collector strategy used to parse ATX style headers that have
    AnchorHub tags specified

    ATX style headers begin with 1-5 hash '#' characters, and then use
    the rest of the line to specify the text of the header. For example:

    # This is an ATX header!
    ### So is this!
    """
    def __init__(self, opts):
        """
        Initializes the object to utilize the AnchorHub tag wrapper
        as specified.

        :param opts: Namespace with the attribute 'wrapper_pattern',
            typically obtained through command-line argument parsing
        """
        self._open = opts.open
        self._close = opts.close
        self._header_pattern = r"^#+ .+" + opts.wrapper_regex + r"\s*$"
        self._regex = re.compile(self._header_pattern, re.UNICODE)

    def test(self, file_lines, index):
        """
        Is this line an ATX header with an AnchorHub tag specified? Return
        True if it is.

        :param file_lines: List of strings corresponding to lines in a text file
        :param index: index of file_lines corresponding to the current line
        :return: True if the line in file_lines at index is an ATX header
            with an AnchorHub tag declared. False otherwise
        """
        return self._regex.match(file_lines[index])

    def get(self, file_lines, index):
        """
        Extract the specified AnchorHub tag, as well as the portion of the
        line that should be converted from the ATX style Markdown header.

        :param file_lines: List of strings corresponding to lines in a text file
        :param index: index of file_lines corresponding to the current line
        :return: [tag, string] - tag: the extracted AnchorHub tag. string -
            the portion of the header that should be converted into an anchor
        """
        line = file_lines[index]
        start_index = line.find('# ') + 2   # Start index for header text
        start_tag = line.rfind(self._open)  # Start index of AnchorHub tag
        end_tag = line.rfind(self._close)   # End index of AnchorHub tag

        # The magic '+1' below knocks out the hash '#' character from extraction
        tag = line[start_tag + len(self._open) + 1:end_tag]
        string = line[start_index:start_tag]
        return [tag, string]


class MarkdownSetextCollectorStrategy(CollectorStrategy):
    """
    Concrete collector strategy used to parse Setext style headers that have
    AnchorHub tags specified

    Setext style headers are 'underlined' with a line comprised entirely of
    equals-signs or hyphens. These are valid Setext headers:

        This is an H1 header
        ====================

        This is an H2 header
        -

    Note that the underlining characters are mutually exclusive. This is
    _not_ a valid header:

        This is not a header
        ====----
    """
    def __init__(self, opts):
        """
        Initializes the object to utilize the AnchorHub tag wrapper
        as specified.

        :param opts: Namespace with the attribute 'wrapper_pattern',
            typically obtained through command-line argument parsing
        """
        self._open = opts.open
        self._close = opts.close
        self._header_pattern = opts.wrapper_regex + r"\s*$"
        self._header_regex = re.compile(self._header_pattern, re.UNICODE)
        self._underline_regex = re.compile(mdrx.setext_underline)

    def test(self, file_lines, index):
        """
        This is line a Setext header with an AnchorHub tag specified? Return
        True if it is.

        file_lines and index _must_ be provided to this function, or it will
        throw a ValueError


        :param file_lines: list of strings corresponding to lines in a text file
        :param index: index of file_lines corresponding to the current line
        :return: True if the line in line_files at index is a Setext header
            with an AnchorHub tag declared. False otherwise
        """
        if file_lines is None: raise ValueError("file_lines list must be "
                                                "provided to test() method in "
                                                "MarkdownSetextCollectorStrategy")
        if index is None: raise ValueError("index must be provided to test() "
                                           "method in "
                                           "MarkdownSetextCollectorStrategy")

        # If index is at len(file_lines) - 1, it's the last line in file
        # Since it needs an underline, cannot be a header
        index_in_bounds = index < len(file_lines) - 1

        if (index_in_bounds and self._header_regex.search(file_lines[index]) and
                self._underline_regex.match(file_lines[index+1])):
            return True
        else:
            return False

    def get(self, file_lines, index):
        """
        Extract the specified AnchorHub tag, as well as the portion of the
        line that should be converted from the ATX style Markdown header.

        :param file_lines: List of strings corresponding to lines in a text file
        :param index: index of file_lines corresponding to the current line
        :return: [tag, string] - tag: the extracted AnchorHub tag. string -
            the portion of the header that should be converted into an anchor
        """
        line = file_lines[index]
        start_tag = line.rfind(self._open)  # Start index of AnchorHub tag
        end_tag = line.rfind(self._close)   # End index of AnchorHub tag

        # The magic '+1' below knocks out the hash '#' character from extraction
        tag = line[start_tag + len(self._open) + 1:end_tag]
        string = line[:start_tag]
        return [tag, string]

