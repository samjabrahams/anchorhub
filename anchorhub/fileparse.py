"""
fileparse.py - Functions for obtaining a list of string file paths according
to input options
"""
import os.path

from anchorhub.util.getfiles import get_files


def get_file_list(opts):
    """
    Returns a list containing file paths of requested files to be parsed
    using AnchorHub options.

    :param opts: Namespace containing AnchorHub options, usually created from
        command line arguments
    :return: a list of absolute string file paths of files that should be
        parsed
    """
    if opts.is_dir:
        # Input is a directory, get a list of files
        return get_files(opts.abs_input, opts.extensions, exclude=[
            opts.abs_output], recursive=opts.recursive)
    elif os.path.isfile(opts.input):
        # Input is a file, should only parse that one file
        return [opts.abs_input]
    else:
        # Input is non-existent
        return []
