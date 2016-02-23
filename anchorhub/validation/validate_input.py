"""
Functions for validating input passed in as an argument to AnchorHub
"""
import os.path
from anchorhub.exceptions.validationexception import ValidationException


def validate(opts):
    """
    Client-facing validate method. Checks to see if the passed in opts
    argument is a namespace containing an attribute named 'input',
    and validates accordingly.

    :param opts: A namespace containing the attribute 'input'
    :raises: ValidationException: if the input fails validation
    :raises: ValueError: if opts does not have the attribute 'input'
    :return: True if the input passes validation
    """
    if hasattr(opts, 'input'):
        return _validate(opts.input)
    else:
        raise ValueError("Options object opts must contain the attribute "
                         "'input'")


def _validate(path):
    """

    :param path: string file path
    :raises ValidationException: if the path fails validation
    :return: True if the path passes validation
    """
    validate_path_exists(path)
    return True


def validate_path_exists(path):
    """
    Returns True of the path exists, throws a ValidationException otherwise
    :param path: String file path
    :raises ValidationException: if the path does not exist
    :return: True if the path exist. Raises a ValidationException otherwise
    """
    if os.path.exists(path):
        return True
    else:
        raise ValidationException("Provided input (" + path + ") does not "
                                  "exist.")
