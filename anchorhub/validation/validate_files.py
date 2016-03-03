"""
Validations for lists of file paths.
"""
import sys

from anchorhub.exceptions.validationexception import ValidationException
import anchorhub.messages as messages


def validate(file_paths, opts):
    """
    Client facing validate function. Runs _validate() and returns True if the
    the file_paths pass all of the validations. Handles exceptions
    automatically if _validate() throws any and exits the program.

    :param file_paths: List of string file paths to test
    :param opts: command-line arguments namespace - used for creating useful
        messages to the client if any tests fail
    :return: True if the file passes all validation tests
    """
    try:
        return _validate(file_paths)
    except ValidationException as e:
        if str(e) == "No files found":
            messages.print_no_files_found(opts)
        else:
            print(e)
        sys.exit(0)


def _validate(file_paths):
    """
    _validate() runs tests on a list of file paths.

    :param file_paths: List of string file paths to test
    :raises ValidationException: if any validation tests fail
    :return: True if all validations pass
    """
    if all([is_not_empty(file_paths)]):
        return True
    else:
        raise ValidationException("File paths did not pass validation.")


def is_not_empty(file_paths):
    """
    Tests to ensure the list of file paths is not empty.

    :param file_paths: List of string file paths to test
    :raises ValidationException: if the list is empty
    :return: True if the list is not empty
    """
    if len(file_paths) < 1:
        raise ValidationException("No files found")
    else:
        return True
