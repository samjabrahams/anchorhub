"""
validate_opts.py - Functions for validating parsed command line arguments.
"""
import sys

import anchorhub.validation.validate_input as vi
import anchorhub.validation.validate_extensions as ve
import anchorhub.validation.validate_overwrite as vo
import anchorhub.validation.validate_wrapper as vw
from anchorhub.exceptions.validationexception import ValidationException


def validate(opts):
    """
    Client facing validate function for command line arguments.

    Perform validation operations on opts, a namespace created from
    command line arguments. Returns True if all validation tests are successful.
    If an exception is raised by the validations, this gracefully exits the
    program and leaves a message to the user.

    Required attributes on opts:
    * input: String giving the path to input files
    * output: String giving the path to output destination
    * wrapper: String specifying the wrapper format
    * extensions: List of strings specifying the file extensions to look for
    * overwrite: Boolean specifying whether the original input files should
                 be overridden

    :param opts: namespace containing necessary parameters
    :return: True, if all tests are successful
    """
    try:
        return _validate(opts)
    except ValidationException as e:
        print("Command line arguments failed validation:")
        print(e)
        sys.exit(0)
    except ValueError as e:
        print("Incorrect type passed into anchorhub.validate_opts.validate()\n")
        print(e)
        sys.exit(0)


def _validate(opts):
    """
    Perform validation operations on opts, a namespace created from
    command-line arguments. Returns True if all validation tests are successful.

    Runs validation() methods in validate_input.py, validate_extensions.py,
    validate_overwrite.py, and validate_wrapper.py

    Required attributes on opts:
    * input: String giving the path to input files
    * output: String giving the path to output destination
    * wrapper: String specifying the wrapper format
    * extensions: List of strings specifying the file extensions to look for
    * overwrite: Boolean specifying whether the original input files should
                 be overridden

    :param opts: namespace containing necessary parameters
    :raises ValidationException: if one or more of the tests are unsuccessful
    :raises ValueError: if opts is not a namespace with the correct parameters
    :return: True, if all tests are successful
    """
    if all([vi.validate(opts),
            ve.validate(opts),
            vw.validate(opts),
            vo.validate(opts)]):
        return True
    else:
        raise ValidationException("Arguments did not pass validation. Check "
                                  "your inputs.")
