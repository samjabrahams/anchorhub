"""
File that initializes a Collector object designed for GitHub style markdown
files.
"""

from anchorhub.collector import Collector
from anchorhub.builtin.github.cstrategies import \
    MarkdownATXCollectorStrategy, MarkdownSetextCollectorStrategy
import anchorhub.builtin.github.converter as converter
import anchorhub.builtin.github.switches as ghswitches


def make_github_markdown_collector(opts):
    """
    Creates a Collector object used for parsing Markdown files with a GitHub
    style anchor transformation

    :param opts: Namespace object of options for the AnchorHub program.
    Usually created from command-line arguments. It must contain a
    'wrapper_regex' attribute
    :return: a Collector object designed for collecting tag/anchor pairs from
    Markdown files using GitHub style anchors
    """
    assert hasattr(opts, 'wrapper_regex')
    atx = MarkdownATXCollectorStrategy(opts)
    setext = MarkdownSetextCollectorStrategy(opts)
    code_block_switch = ghswitches.code_block_switch

    strategies = [atx, setext]
    switches = [code_block_switch]

    return Collector(converter.create_anchor_from_header, strategies,
                     switches=switches)
