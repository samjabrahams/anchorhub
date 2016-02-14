"""
Tests for GitHub style anchor generator
"""

from anchorhub.builtin.github.converter import create_anchor_from_header


def test_github_converter():
    """
    Built-in: Test GitHub anchor generator
    """
    a = create_anchor_from_header("this is a--- --- test!!!")
    assert a == "this-is-a--------test"

    b = create_anchor_from_header("this.is/the'second'test")
    assert b == "thisisthesecondtest"

    c = create_anchor_from_header("this is a third test ... ... %")
    assert c == "this-is-a-third-test---"

    d = create_anchor_from_header(
            "now_we_are testing underscores------%-------")
    assert d == "now_we_are-testing-underscores-------------"

    e = create_anchor_from_header(
        "what%#$about multiple...//()(odd characters between$$#@!/,.,.';'\"["
        "][[[[]}{words?")
    assert e == "whatabout-multipleodd-characters-betweenwords"

    f = create_anchor_from_header(
            "Header ends with ellipses, but anchor ends with hyphen? ...")
    assert f == "header-ends-with-ellipses-but-anchor-ends-with-hyphen-"

    g = create_anchor_from_header("THIS HEADER## HAS ## HASHTAG###SS")
    assert g == "this-header-has--hashtagss"
