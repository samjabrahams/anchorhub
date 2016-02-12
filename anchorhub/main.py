"""
Command-line entry to AnchorHub, main method is here.
"""

import anchorhub.cmdparse as cmdparse
import anchorhub.messages as messages
import anchorhub.normalization.normalize_opts as normalize_opts
import anchorhub.validation.validate_opts as validation
from anchorhub.util.getfiles import get_files


def main(argv=None):
    """
    Main entry method for AnchorHub. Takes in command-line arguments,
    finds files to parse within the specified input directory, and outputs
    parsed files to the specified output directory.

    :param argv: a list of string command line arguments
    """
    # Get command line arguments, validate them, and normalize them
    opts = cmdparse.parse_args(argv)
    assert validation.validate(opts)
    opts = normalize_opts.normalize(opts)

    # Update client: print input and output directories
    messages.print_directories(opts)

    file_paths = get_files(opts.abs_input, opts.extensions,
                           exclude=[opts.abs_output])

    print file_paths

if __name__ == '__main__':
    main()