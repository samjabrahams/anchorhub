"""
File for GitHub style anchor generation
"""
import re


def create_anchor_from_header(header, existing_anchors=None):
    """
    Creates GitHub style auto-generated anchor tags from header line strings

    :param header: The portion of the line that should be converted
    :param existing_anchors: A dictionary of AnchorHub tags to auto-generated
        anchors
    :return: A string auto-generated anchor in the GitHub format
    """
    # Strip white space on the left/right and make lower case
    out = header.strip().lower()

    # Replace groups of white space with hyphens
    out = re.sub(r"\s+", lambda x: "-", out, flags=re.UNICODE)

    # Remove characters that aren't alphanumeric, hyphens, or spaces
    out = re.sub(r"[^\w\- ]+", lambda x: "", out, flags=re.UNICODE)
    if existing_anchors and out in existing_anchors.values():
        i = 1
        while (out + "-" + str(i)) in existing_anchors:
            i += 1
        return out + "-" + str(i)
    else:
        return out
