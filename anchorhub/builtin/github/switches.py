"""
File for GitHub markdown switches
"""
from anchorhub.lib.armedcheckswitch import ArmedCheckSwitch
from anchorhub.lib.lazyregex import LazyRegex
import anchorhub.builtin.regex.markdown as mdrx


# LazyRegex objects for testing if a line indicates the start of a code block
# Or the end of a code block
code_start = LazyRegex(mdrx.code_block_start)
code_end = LazyRegex(mdrx.code_block_end)


def code_block_start_test(lines, index):
    """
    Tests to see if the line at the current index of lines indicates the
    start of a Markdown code block.

    :param lines: List of strings, with each entry corresponding to a single
        line in a text file
    :param index: The current line in lines
    :return: True if the current line indicates the start of a code block
    """
    return code_start.match(lines[index])


def code_block_end_test(lines, index):
    """
    Tests to see if the line at the current index of lines indicates the
    end of a Markdown code block.

    :param lines: List of strings, with each entry corresponding to a single
        line in a text file
    :param index: The current line in lines
    :return: True if the current line indicates the end of a code block
    """
    return code_end.match(lines[index])


code_block_switch = ArmedCheckSwitch(on_check=code_block_start_test,
                                     off_check=code_block_end_test)
