"""
File that initializes a Writer object designed for GitHub style markdown files.
"""

from anchorhub.writer import Writer
from anchorhub.builtin.github.wstrategies import MarkdownATXWriterStrategy, \
    MarkdownSetextWriterStrategy, MarkdownInlineLinkWriterStrategy, \
    MarkdownReferenceLinkWriterStrategy
import anchorhub.builtin.github.switches as ghswitches


def make_github_markdown_writer(opts):
    """
    Creates a Writer object used for parsing and writing Markdown files with
    a GitHub style anchor transformation

    opts is a namespace object containing runtime options. It should
    generally include the following attributes:

    * 'open':   a string corresponding to the opening portion of the wrapper
                identifier. Built-in AnchorHub usage defaults this to '{'
    * 'close:   a string corresponding ot the closing portion of the wrapper
                identifier. Built-in AnchorHub usage defaults this to '}'
    * 'wrapper_regex':  An escaped regular expression that matches tags
                        located inside of wrappers

    :param opts: namespace object, usually created from command-line
        arguments, that is used to pass runtime options to concrete
        WriterStrategy objects.
    :return: A Writer object designed for parsing, modifying, and writing
        AnchorHub tags to converted anchors in Markdown files using GitHub style
        anchors
    """
    assert hasattr(opts, 'wrapper_regex')
    atx = MarkdownATXWriterStrategy(opts, 'ATX headers')
    setext = MarkdownSetextWriterStrategy(opts, 'Setext headers')
    inline = MarkdownInlineLinkWriterStrategy(opts, 'inline links')
    ref = MarkdownReferenceLinkWriterStrategy(opts, 'reference links')
    code_block_switch = ghswitches.code_block_switch

    strategies = [atx, setext, inline, ref]
    switches = [code_block_switch]

    return Writer(strategies, switches=switches)