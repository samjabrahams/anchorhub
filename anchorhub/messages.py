"""
messages.py - Functions that print out messages to the console
"""
from anchorhub.util.stripprefix import strip_prefix


def print_directories(opts):
    """
    Prints the input and output directories to the console.

    :param opts: namespace that contains printable 'input' and 'output' fields.
    """
    print("Root input directory: \t" + opts.input)
    print("Outputting to: \t\t" + opts.output + "\r\n")


def print_files(opts, file_paths):
    """
    Prints the file paths that will be parsed.

    :param file_paths:
    """
    print("Parsing the following files:")
    for file_path in file_paths:
        print("  " + strip_prefix(file_path, opts.abs_input))
    print("--------------------")
    print(str(len(file_paths)) + " files total\n")


def print_no_files_found(opts):
    msg =  "No files found with [" +', '.join(opts.extensions) + "] "
    msg += "extension" +("s " if len(opts.extensions) > 1 else " ")
    msg += "in " + opts.input
    # if recursive
    msg += " or any of its subdirectories"
    print(msg)
