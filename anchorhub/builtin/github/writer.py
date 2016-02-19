"""
File that initializes a Writer object designed for GitHub style markdown files.
"""

from anchorhub.writer import Writer
from anchorhub.builtin.github.wstrategies import MarkdownATXWriterStrategy, \
    MarkdownSetextWriterStrategy, MarkdownInlineLinkWriterStrategy
import anchorhub.builtin.github.switches as ghswitches


def make_github_markdown_writer(opts):
    """
    Creates a Writer object used for parsing and writing Markdown files with
    a GitHub style anchor transformation

    :param opts:
    :return: A Writer object designed for parsing, modifying, and writing
    AnchorHub tags to converted anchors in Markdown files using GitHub style
    anchors
    """
    assert hasattr(opts, 'wrapper_regex')
    atx = MarkdownATXWriterStrategy(opts)
    inline = MarkdownInlineLinkWriterStrategy(opts)
    code_block_switch = ghswitches.code_block_switch

    strategies = [atx, inline]
    switches = [code_block_switch]

    return Writer(strategies, switches=switches)