"""
Regular expression patterns for Markdown files.

Names of regex variables in this file:
anchor_link
ref_link
setext_underline
code_block_start
code_block_end

Markdown:
https://daringfireball.net/projects/markdown/syntax
"""

"""
anchor_link: Inline Markdown link that uses an anchor tag

Has the following specification:

1. A set of square brackets '[]', containing at least one character
2. Followed by any amount of whitespace (or none)
3. Followed by an opening parenthesis '('
4. Followed by any amount of whitespace (or none)
5. Followed by an optional string of non-whitespace, non-closing parenthesis ')'
        characters
6. Followed by a hash '#' character
7. Followed by a string of non-whitespace, non-closing parenthesis ')' characters
8. Followed by any amount of whitespace (or none)
9. Followed by a closing parenthesis ')'

Number 5 above corresponds to the URL/path portion of the link, such as
'anotherfile.md'. Number 7 above corresponds to the anchor tag, which may or
may not be an AnchorHub tag.

Examples of matching patterns:

    [This is the link text!](file.md#tag)
    [White space in the middle works]     (#tag)
    [Also white space inside the parenthesis will work](    #likethis    )

Note: while the repeated 'any white space' commands may make the final regex
pattern more obnoxious, it makes its use more flexible. AnchorHub strives to
not enforce an opinion on syntax- if it renders as Markdown, it should work
in AnchorHub.
"""
anchor_link = r"\["         # opening square bracket
anchor_link += r"[^\[\]]+"  # at least one non-square bracket char
anchor_link += r"\]"        # closing square bracket
anchor_link += r"\s*"       # any amount of whitespace
anchor_link += r"\("        # an opening parenthesis '('
anchor_link += r"\s*"       # any amount of whitespace
anchor_link += r"[^\s\)]*"  # Optional string of non-whitespace, non-')' chars
anchor_link += r"#"         # A hash '#' character
anchor_link += r"[^\s\)]+"  # A string of non-whitespace, non-')' chars
anchor_link += r"\s*"       # any amount of whitespace
anchor_link += r"\)"        # A closing parenthesis ')'


"""
anchor_link_start: The first portion of an inline link, before the URL

Useful for getting the string indices of different parts of the link.

See steps 1-3 of 'anchor_link' above for specifics on the regular expression
components.
"""
anchor_link_start = r"\[.+\]\s*\("

"""
reference_link: Markdown reference link that uses an anchor tag

Has the following specification:

1. A start of line, followed by up to three spaces or tabs
2. Followed by a set of square brackets [], containing at least one character
3. Followed by a colon ':'
4. Followed by one or more white space characters
5. Followed by an optional string of non-whitespace characters
6. Followed by a hash '#' character
7. Followed by one or more non-whitespace characters

Number 5 above corresponds to the URL/path portion of the link, such as
'anotherfile.md'. Number 7 above corresponds to the anchor tag, which may or
may not be an AnchorHub tag.

Examples of matching patterns:

    [ref]: somefile.md#tag
    [ref]: #hastitle "Here is a title for my link!"
"""
ref_link = r"^[ \t]{0,3}"   # Start of line, followed by up to 3 spaces/tabs
ref_link += r"\[.+\]"       # square brackets containing at least one char
ref_link += r":"            # A colon ':' character
ref_link += r"\s+"          # One or more whitespace characters
ref_link += r"\S*"          # Optional string of non-whitespace characters
ref_link += r"#"            # Hash '#' character
ref_link += r"\S+"          # One or more non-whitespace characters


"""
setext_underline: Markdown Setext style header underline

Markdown supports two styles of header syntax: Setext and ATX. Setext style
headers are "underlined" with either equal signs or hyphens

The following syntax matches the following:

1. A start of line
2. Followed by a series of one or more hyphens XOR equal signs
3. Followed by any amount of whitespace
4. Followed by an end of line

So it will match these:
    ---------
    ====

But it will not match this:
    ---===

"""
setext_underline = r"^"             # Start of line
setext_underline += r"([-=])\1*"    # One or more hyphen '-' or equal sign '='
setext_underline += r"\s*"          # Any amount of whitespace
setext_underline += r"$"            # End of line


"""
code_block_start, code_block_end: demarcation of code block sections in Markdown

The triple backtick '`' is used to mark the beginning and end of code blocks in
markdown. However, the pattern for code_block_start is less restrictive as
many Markdown parsers allow users to specify the code format just after the
back ticks. Therefore, the specification for the opening and closing markers
are slightly different.

code_block_start:

1. A start of line
2. Followed by 3 backticks '`' in a row

code_block_end:

1. A start of line
2. Followed by 3 backticks '`' in a row
3. Followed by any amount of whitespace
4. Followed by an end of line
"""

code_block_start = r"^"     # Start of line
code_block_start += r"```"  # Series of 3 backticks

code_block_end = r"^"       # Start of line
code_block_end += r"```"    # Series of 3 backticks
code_block_end += r"\s*"    # Any amount of whitespace
code_block_end += r"$"      # End of line

