"""
Concrete CollectorStrategy classes for the GitHub built-in module
"""
import re

from anchorhub.collector import CollectorStrategy


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
        super(MarkdownATXCollectorStrategy, self).__init__()
        self._open = opts.open
        self._close = opts.close
        self._header_pattern = r"^#+ .+" + opts.wrapper_regex + r"\s*$"
        self._regex = re.compile(self._header_pattern)

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
