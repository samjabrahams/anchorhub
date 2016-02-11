"""
Functions for validating the overwrite argument in combination with other
arguments
"""
import os.path as path

from anchorhub.exceptions.validationexception import ValidationException
from anchorhub.util.hasattrs import hasattrs


def validate(opts):
    """
     Client facing overwrite validation. Checks to see if the opts arguments
     contains the attributes 'overwrite', 'input', and 'output'.

    :param opts: a namespace containing the attributes 'overwrite', 'input',
        and 'output'
    :raises ValueError: if the value passed in is not a namespace with the
        attributes 'overwrite', 'input', and 'output'
    :raises ValidationException: if opts fails any of the validations
    :return: True if opts passes the validations
    """
    if hasattrs(opts, 'overwrite', 'input', 'output'):
        return _validate(opts)
    else:
        raise ValueError("opts object must have attributes 'overwrite', "
                         "'input', and 'output.")


def _validate(opts):
    """
    Runs validation functions on a namespace containing the attributes
    'overwrite' (boolean), 'input' (string), and 'output' (string).

    :param opts: a namespace containing the attributes 'overwrite', 'input',
        and 'output'
    :raises ValidationException: if opts fails any of the validations
    :return: True if opts passes the validations
    """
    validate_overwrite_different_input_output(opts)
    return True


def validate_overwrite_different_input_output(opts):
    """
    Make sure that if overwrite is set to False, the input and output folders
    are not set to the same location.

    :param opts: a namespace containing the attributes 'overwrite', 'input',
        and 'output'
    :raises ValidationException: if 'input' and 'output' point to the same
        directory and 'overwrite' is set to False
    :return: True if 'overwrite' is set to True, or 'input'/'output' are
        separate directories
    """
    if opts.overwrite or path.abspath(opts.input) != path.abspath(opts.output):
        return True
    else:
        raise ValidationException("Input and output directories are the same, "
                                  "but --overwrite / -X flag is not provided.\n"
                                  "Do you want to overwrite your input files? "
                                  "If so, use the following command:\n"
                                  "\tanchorhub -X " + opts.input)
