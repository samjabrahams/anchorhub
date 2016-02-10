"""
Functions for validating the wrapper passed in as arguments to AnchorHub
"""
from anchorhub.exceptions.validationexception import ValidationException


def validate(opts):
    """
    Client-facing validate method. Checks to see if the passed int opts
    argument is either a string or a namespace containing the attribute
    'wrapper' and runs validations on it accordingly.

    Note: this function currently does NOT support Unicode/Byte style strings,
    will need to do some work on Python 2/Python 3 compatibililty to add this
    in.

    :param opts: either a string or a namespace with the attribute 'extensions'
    :raises ValueError: if the value passed in is not a string or a namespace
        with the attribute 'wrapper'
    :raises ValidationException: if the wrapper fail validations
    :return: True if wrapper passes the validations
    """
    if hasattr(opts, 'wrapper') and isinstance(opts.wrapper, str):
        return _validate(opts.wrapper)
    elif isinstance(opts, str):
        return _validate(opts)
    else:
        raise ValueError("Argument passed into wrapper validation must either "
                         "be a single (non-Unicode) string, or a namespace "
                         "with an attribute of 'wrapper'")


def _validate(wrapper):
    """
    Performs validations on a list of extensions. Raises a
    ValidationException if it finds something wrong.

    :param wrapper: a wrapper-defining string
    :raises ValidationException: if the wrapper fails any of the validations
    :return: True if wrapper passes the validations
    """
    validate_two_components(wrapper)
    return True


def validate_two_components(wrapper):
    """
    Make sure that the string defining the wrapper is formatted as two
    'words'. Basically, it should have the format "{open} {close}" with some
    form of white space between the opening and closing patterns. It should
    also have no more than two 'words'

    :param wrapper: String that defines a wrapper
    :raises ValidationException: if wrapper is not formatted correctly
    :return: True if the wrapper is formatted correctly
    """
    if len(wrapper.split()) != 2:
        raise ValidationException("Header demarcation must be of the form \n\t"
                                  "'{startpattern} {stoppattern}'\n"
                                  "(Note the space between the two patterns")
    return True
