"""
Tests for GitHub builtin collector strategies
"""

import anchorhub.builtin.github.cstrategies as cstrategies
import anchorhub.cmdparse as cmdparse
import anchorhub.normalization.normalize_opts as normalize_opts


def test_atx_collector_strategy():
    """
    GitHub Built-in: Test MarkdownATXCollectorStrategy with defaults
    """
    opts = normalize_opts.normalize(cmdparse.parse_args(['.']))
    s = cstrategies.MarkdownATXCollectorStrategy(opts)

    lines = [
        "# This is my first test {#test1}",
        "This should not match",
        "### This should also not match",
        "#### This one should match though! {#test4}"
        ]
    assert s.test(lines, 0)
    assert not s.test(lines, 1)
    assert not s.test(lines, 2)
    assert s.test(lines, 3)

    assert s.get(lines, 0) == ['test1', 'This is my first test ']
    assert s.get(lines, 3) == ['test4', 'This one should match though! ']


def test_atx_collector_strategy_different_wrapper():
    """
    GitHub Built-in: Test MarkdownATXCollectorStrategy with different wrapper
    """
    opts = normalize_opts.normalize(cmdparse.parse_args(['.', '-w' '[> <]']))
    s = cstrategies.MarkdownATXCollectorStrategy(opts)

    lines = [
        "# This is my first test [>#test1<]",
        "This should not match",
        "### This should also not match",
        "#### This one should match though! [>#test4<]"
    ]
    assert s.test(lines, 0)
    assert not s.test(lines, 1)
    assert not s.test(lines, 2)
    assert s.test(lines, 3)

    assert s.get(lines, 0) == ['test1', 'This is my first test ']
    assert s.get(lines, 3) == ['test4', 'This one should match though! ']


