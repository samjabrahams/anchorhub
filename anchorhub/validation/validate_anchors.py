"""
Validations for anchors and tags found during collection.
"""

import sys

from anchorhub.exceptions.validationexception import ValidationException
import anchorhub.messages as messages


def validate(anchors, duplicate_tags, opts):
    """
    Client facing validate function. Runs _validate() and returns True if
    anchors and duplicate_tags pass all validations. Handles exceptions
    automatically if _validate() throws any and exits the program.

    :param anchors: Dictionary mapping string file path keys to dictionary
        values. The inner dictionaries map string AnchorHub tags to generated
        anchor values
    :param duplicate_tags: Dictionary mapping string file path keys to a list of
        tuples. The tuples contain the following information, in order:

        1. The string AnchorHub tag that was repeated
        2. The line in the file that the duplicate was found, as a number
        3. The string generated anchor that first used the repeated tag
    :param opts: Namespace containing AnchorHub options, usually created by
        command line arguments
    :return: True if the anchors pass all validation tests
    """
    try:
        return _validate(anchors, duplicate_tags, opts)
    except ValidationException as e:
        if str(e) == "Duplicate tags found":
            messages.print_duplicate_anchor_information(duplicate_tags)
        else:
            print(e)
        sys.exit(0)


def _validate(anchors, duplicate_tags, opts):
    """
    Runs set of validations on collected AnchorHub tags and generated anchors

    :param anchors: Dictionary mapping string file path keys to dictionary
        values. The inner dictionaries map string AnchorHub tags to generated
        anchor values
    :param duplicate_tags: Dictionary mapping string file path keys to a list of
        tuples. The tuples contain the following information, in order:

        1. The string AnchorHub tag that was repeated
        2. The line in the file that the duplicate was found, as a number
        3. The string generated anchor that first used the repeated tag
    :param opts: Namespace containing AnchorHub options, usually created by
        command line arguments
    :raises ValidationException: if any of the validations fail
    :return: True if the anchors pass all validation tests
    """
    if all([no_duplicate_tags(duplicate_tags)]):
        return True
    else:
        raise ValidationException("File paths did not pass validation.")


def no_duplicate_tags(duplicate_tags):
    """
    Tests to make sure that the list of duplicate tags is empty.

    :param duplicate_tags: Dictionary mapping string file path keys to a list of
        tuples. The tuples contain the following information, in order:

        1. The string AnchorHub tag that was repeated
        2. The line in the file that the duplicate was found, as a number
        3. The string generated anchor that first used the repeated tag
    :raises ValidationException: If the list of duplicate tags is not empty
    :return: True if the list of duplicate tags is empty
    """
    if len(duplicate_tags) > 0:
        raise ValidationException("Duplicate tags found")
    else:
        return True
