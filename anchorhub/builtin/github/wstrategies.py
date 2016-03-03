"""
Concrete WriteStrategy classes for the GitHub built-in module
"""
import re
import os
import os.path

import anchorhub.builtin.regex.markdown as mdrx
from anchorhub.writer import WriterStrategy


class MarkdownATXWriterStrategy(WriterStrategy):
    """
    Concrete writer used to remove AnchorHub tags from ATX style Markdown
    headers.

    ATX style headers begin with 1-5 hash '#' characters, and then use
    the rest of the line to specify the text of the header. For example:

        # This is an ATX header!
        ### So is this!

What this strategy does is convert a header from this:
        # My awesome header {#cool}
    Into this:
        # My awesome header
    """
    def __init__(self, opts, label=None):
        """
        Initializes the object to utilize the AnchorHub tag wrapper
        as specified.

        :param opts: Namespace with the attributes 'wrapper_pattern', 'open',
            and 'close' typically obtained through command-line argument parsing
        """
        super(MarkdownATXWriterStrategy, self).__init__(opts, label)
        self._open = opts.open
        self._close = opts.close
        self._header_pattern = r"^#+ .+" + opts.wrapper_regex + r"\s*$"
        self._regex = re.compile(self._header_pattern, re.UNICODE)
        self._label = label

    def test(self, current_modified_line, file_lines=None, index=None):
        """
        Is this line an ATX header with an AnchorHub tag specified? Return
        True if it is.

        :param current_modified_line: string representing the the line at
            file_lines[index] _after_ any previous modifications from other
            WriterStrategy objects
        :param file_lines: List of strings corresponding to lines in a text file
        :param index: index of file_lines corresponding to the current line
        :return: True if current_modified_line is an ATX header with an
        AnchorHub tag declared. False otherwise
        """
        return self._regex.match(current_modified_line)

    def modify(self, current_modified_line, anchors, file_path, file_lines=None,
               index=None):
        """
        Removes the trailing AnchorHub tag from the end of the line being
        examined.

        :param current_modified_line: string representing the the line at
            file_lines[index] _after_ any previous modifications from other
            WriterStrategy objects
        :param anchors: Dictionary mapping string file paths to inner
            dictionaries. These inner dictionaries map string AnchorHub tags
            to string generated anchors
        :param file_path: string representing the file_path of the current
            file being examined by this WriterStrategy
        :param file_lines: List of strings corresponding to lines in a text file
        :param index: index of file_lines corresponding to the current line
        :return: string. A version of current_modified_line that has the
            AnchorHub tag removed from the end of it
        """
        open_wrapper_index = current_modified_line.rfind(self._open)
        # '- 1' removes trailing space. May want to modify to completely
        # strip whitespace at the end, instead of only working for a single
        # space
        return current_modified_line[:open_wrapper_index - 1] + "\n"


class MarkdownSetextWriterStrategy(WriterStrategy):
    """
    Concrete writer used to remove AnchorHub tags from Setext style Markdown
    headers.

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

    With default AnchorHub settings, this writer will convert this:

        This header has an AnchorHub tag! {#tag}

    Into this:

        This header has an AnchorHub tag!
    """
    def __init__(self, opts, label=None):
        """
        Initializes the WriterStrategy to utilize the AnchorHub tag wrapper
        as specified.

        :param opts: Namespace with the attributes 'wrapper_pattern', 'open',
            and 'close' typically obtained through command-line argument parsing
        """
        super(MarkdownSetextWriterStrategy, self).__init__(opts, label)
        self._open = opts.open
        self._close = opts.close
        self._header_pattern = opts.wrapper_regex + r"\s*$"
        self._header_regex = re.compile(self._header_pattern, re.UNICODE)
        self._underline_regex = re.compile(mdrx.setext_underline, re.UNICODE)

    def test(self, current_modified_line, file_lines=None, index=None):
        """
        This is line a Setext header with an AnchorHub tag specified? Return
        True if it is.

        file_lines and index _must_ be provided to this function, or it will
        throw a ValueError

        :param current_modified_line: string representing the the line at
            file_lines[index] _after_ any previous modifications from other
            WriterStrategy objects
        :param file_lines: List of strings corresponding to lines in a text file
        :param index: index of file_lines corresponding to the current line:
        :return: True if current_modified_line is a Setext header with an
        AnchorHub tag declared. False otherwise
        """
        if file_lines is None:
            raise ValueError("file_lines list must be provided to test() method"
                             " in MarkdownSetextWriterStrategy")
        if index is None:
            raise ValueError("index must be provided to test() method in "
                             "MarkdownSetextWriterStrategy")

        # If index is at len(file_lines) - 1, it's the last line in file
        # Since it needs an underline, cannot be a header
        index_in_bounds = index < len(file_lines) - 1

        if (self._header_regex.search(current_modified_line) and
                self._underline_regex.match(file_lines[index+1]) and
                index_in_bounds):
            return True
        else:
            return False

    def modify(self, current_modified_line, anchors, file_path, file_lines=None,
               index=None):
        """

        :param current_modified_line: string representing the the line at
            file_lines[index] _after_ any previous modifications from other
            WriterStrategy objects
        :param anchors: Dictionary mapping string file paths to inner
            dictionaries. These inner dictionaries map string AnchorHub tags
            to string generated anchors
        :param file_path: string representing the file_path of the current
            file being examined by this WriterStrategy
        :param file_lines: List of strings corresponding to lines in a text file
        :param index: index of file_lines corresponding to the current line
        :return: string. A version of current_modified_line that has the
            AnchorHub tag removed from the end of it
        """
        open_wrapper_index = current_modified_line.rfind(self._open)
        # '- 1' removes trailing space. May want to modify to completely
        # strip whitespace at the end, instead of only working for a single
        # space
        return current_modified_line[:open_wrapper_index - 1] + "\n"


class MarkdownInlineLinkWriterStrategy(WriterStrategy):
    """
    Concrete writer used to change inline links that use AnchorHub tags to
    instead use the associated auto-generated anchor.

    An inline link (using an AnchorHub tag) has this format:
        [This is the visible text](url#tag)

    If the generated anchor associated with 'tag' was 'this-is-my-header',
    then the above would be converted to this:
        [This is the visible text](url#this-is-my-header)
    """
    def __init__(self, opts, label=None):
        """
        Initializes object regex objects.

        :param opts: AnchorHub options namespace, usually created from
            command-line arguments
        """
        super(MarkdownInlineLinkWriterStrategy, self).__init__(opts, label)
        self._link_regex = re.compile(mdrx.anchor_link, re.UNICODE)
        self._link_start_regex = re.compile(mdrx.anchor_link_start, re.UNICODE)

    def test(self, current_modified_line, file_lines=None, index=None):
        """
        Does current_modified_line contain one or more inline Markdown links
        that use an anchor (i.e. uses a '#' in the link)? Return True if so.

        :param current_modified_line: string representing the the line at
            file_lines[index] _after_ any previous modifications from other
            WriterStrategy objects
        :param file_lines: List of strings corresponding to lines in a text file
        :param index: index of file_lines corresponding to the current line
        :return: True if the current_modified_line contains one or more
            inline anchor links. False otherwise
        """
        return self._link_regex.search(current_modified_line)

    def modify(self, current_modified_line, anchors, file_path, file_lines=None,
               index=None):
        """
        Replace all AnchorHub tag-using inline links in this line and edit
        them to use

        :param current_modified_line: string representing the the line at
            file_lines[index] _after_ any previous modifications from other
            WriterStrategy objects:
        :param anchors: Dictionary mapping string file paths to inner
            dictionaries. These inner dictionaries map string AnchorHub tags
            to string generated anchor
        :param file_path: string representing the file_path of the current
            file being examined by this WriterStrategy
        :param file_lines: List of strings corresponding to lines in a text file
        :param index: index of file_lines corresponding to the current line
        :return: string. current_modified_line with all inline links that use
            AnchorHub tags replaced with their associated generated anchors
        """
        changed_line = ""  # Will be built up piece by piece as we find links
        links = self._get_link_indices(current_modified_line)

        # Used to keep track of what we've parsed in current_modified_line
        last_index = 0

        for link in links:
            # These indices are relative to current_modified_line
            link_start_index = link[0]  # Start index in current_modified_line
            link_end_index = link[1]  # End index in current_modified_line
            link_text = current_modified_line[link_start_index:link_end_index]

            # This index is relative to link_text
            url_start = self._link_start_regex.search(link_text).end()
            url_text = link_text[url_start:len(link_text) - 1].strip()

            # This index is relative to url_text
            hash_index = url_text.find('#')  # index of '#' in url_text

            link_path = url_text[:hash_index]
            tag = url_text[hash_index + 1:]

            if link_path == "":
                # Link points to tag in this file
                file_key = file_path
            else:
                file_key = self._get_file_key(file_path, link_path)

            if self._file_has_tag_anchor_keypair(anchors, file_key, tag):
                # The tag used on this link was specified as an AnchorHub tag
                # Add existing text up to (and including) the # mark
                changed_line += current_modified_line[last_index:
                                                      link_start_index +
                                                      url_start + hash_index+1]
                # Add the the generated anchor, plus a closing parenthesis
                changed_line += anchors[file_key][tag] + ')'
            else:
                # The tag used is a normal anchor tag: don't change it
                changed_line += current_modified_line[last_index:link_end_index]
            last_index = link_end_index
        # Add the end of the line back on
        changed_line += current_modified_line[last_index:]
        return changed_line

    def _get_file_key(self, file_path, link_path):
        """
        Finds the absolute path of link_path relative to file_path. The
        absolute path is the key to anchors dictionary used throughout the
        AnchorHub process

        :param file_path: string file path of the file that contains the link
            being examined
        :param link_path: string. The link URL that we'd like to find the
            absolute path for
        :return: the absolute path of link_path relative to file_path
        """
        if os.path.isabs(link_path):
            return link_path
        else:
            file_dir = os.path.dirname(file_path)
            joined_path = os.path.join(file_dir, link_path)
            return os.path.abspath(joined_path)


    def _get_link_indices(self, current_modified_line):
        """
        Get a list of tuples containing start and end indices of inline
        anchor links

        :param current_modified_line: The line being examined for links
        :return: A list containing tuples of the form (start, end),
        the starting and ending indices of inline anchors links.
        """
        # List of (start_index, end_index) tuples for each link in the line
        links = []
        for m in self._link_regex.finditer(current_modified_line):
            links.append(m.span())
        return links

    def _file_has_tag_anchor_keypair(self, anchors, file_key, tag):
        """
        Is there an AnchorHub tag, 'tag', registered for file 'file_key' in
        'anchors'?

        :param anchors: Dictionary mapping string file paths to inner
            dictionaries. These inner dictionaries map string AnchorHub tags
            to string generated anchors
        :param file_key: The absolute path to the file that may or may not
            have the AnchorHub tag in it. Used as a key to anchors
        :param tag: The string being tested
        :return: True if tag is a valid AnchorHub tag in the file associated
            with 'file_key'
        """
        return file_key in anchors and tag in anchors[file_key]


class MarkdownReferenceLinkWriterStrategy(WriterStrategy):
    """
    Concrete WriterStrategy class used to change Markdown reference links
    that use AnchorHub tags to instead use the associate auto-generated anchor.

    A reference link (with an AnchorHub tag) has this format:
        [ref]: (url#tag) "Optional Title"

    If the generated anchor associated with 'tag' is 'this-is-my-header',
    then the above will be converted to this:
        [ref]: (url#this-is-my-header) "Optional Title"

    Note that AnchorHub, at this time, assumes that any line starting with
    the pattern:
        [ref]: (url#tag)
    Is intended to be a reference link, and doesn't do additional checks to
    see whether or not the optional title line is valid Markdown (i.e. is
    enclosed in one of double-quotes, single-quotes, or parentheses)
    """
    def __init__(self, opts, label=None):
        """

        :param opts:
        :return:
        """
        super(MarkdownReferenceLinkWriterStrategy, self).__init__(opts, label)
        self._ref_regex = re.compile(mdrx.ref_link, re.UNICODE)

    def test(self, current_modified_line, file_lines=None, index=None):
        """

        :param current_modified_line:
        :param file_lines:
        :param index:
        :return:
        """
        return self._ref_regex.match(current_modified_line)

    def modify(self, current_modified_line, anchors, file_path,
               file_lines=None, index=None):
        """

        :param current_modified_line:
        :param anchors:
        :param file_path:
        :param file_lines:
        :param index:
        :return:
        """
        url_text = current_modified_line.split()[1]
        url_start_index = current_modified_line.find(url_text)
        url_end_index = url_start_index + len(url_text)
        hash_index = url_text.find('#')  # index of '#' in url_text
        link_path = url_text[:hash_index]
        tag = url_text[hash_index + 1:]

        if link_path == "":
            # Link points to tag in this file
            file_key = file_path
        else:
            file_key = self._get_file_key(file_path, link_path)

        if self._file_has_tag_anchor_keypair(anchors, file_key, tag):
            # The tag used on this link was specified as an AnchorHub tag
            # Create string to return
            mod = ""
            # Add everything on the line up to (and including) the hash sign
            mod += current_modified_line[:url_start_index + hash_index + 1]
            # Add the associated generated anchor
            mod += anchors[file_key][tag]
            # Add on the rest of the line
            mod += current_modified_line[url_end_index:]
            return mod
        else:
            # The tag used is not an AnchorHub tag: don't change it
            return current_modified_line

    def _get_file_key(self, file_path, link_path):
        """

        :param file_path:
        :param link_path:
        :return:
        """
        if os.path.isabs(link_path):
            return link_path
        else:
            file_dir = os.path.dirname(file_path)
            joined_path = os.path.join(file_dir, link_path)
            return os.path.abspath(joined_path)

    def _file_has_tag_anchor_keypair(self, anchors, file_key, tag):
        """

        :param anchors:
        :param file_key:
        :param tag:
        :return:
        """
        return file_key in anchors and tag in anchors[file_key]