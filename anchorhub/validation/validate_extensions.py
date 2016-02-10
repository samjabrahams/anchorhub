"""
Functions for validating extensions passed in as arguments to AnchorHub
"""


def validate(opts):
    """
    Client-facing validate method. Checks to see if the passed in opts
    argument is either a list or a namespace containing the attribute
    'extensions' and runs validations on it accordingly. If opts is neither
    of those things, this will raise a ValueError

    :param opts:
    :raises ValueError: if the extensions fail validations OR if the value
        passed in is not a list or a namespace with the attribute 'extensions'
    :return: True if extensions pass the validations
    """
    if hasattr(opts, 'extensions'):
        return _validate(opts.extensions)
    elif isinstance(opts, list):
        return _validate(opts)
    else:
        raise ValueError("Value passed into extension validation must either "
                         "be a list of strings or a namespace with an "
                         "attribute of 'extensions'")


def _validate(extensions):
    """
    Perform validations on a list of extensions. Will raise a ValueError if
    it finds something wrong.

    :param extensions: a list of string extensions
    :raises ValueError: if the extensions fail any of the validations
    :return: True if the extensions pass the validations
    """
    validate_no_empty_strings(extensions)
    validate_list_not_empty(extensions)
    return True


def validate_no_empty_strings(extensions):
    """
    Returns True if there are no empty strings in the list of extensions.
    False otherwise.

    :param extensions: a list of string extensions
    :raises ValueError:
    :return: True if no empty strings in list of extensions, raises a
        ValueError otherwise
    """
    if "" not in extensions:
        return True
    else:
        raise ValueError("Empty strings are not valid extensions.")


def validate_list_not_empty(extensions):
    """
    Returns True if the list provided is not empty. False otherwise

    :param extensions: a list of string extensions
    :raises ValueError:
    :return: True if extensions list is not empty. Raises a ValueError
        otherwise
    """
    if len(extensions) > 0:
        return True
    else:
        raise ValueError("You must provide at least one extension.")
