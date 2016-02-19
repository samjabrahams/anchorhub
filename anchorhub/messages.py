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
    """
    Prints message that no files were found in the input directory with the
    given list of extensions.

    :param opts: Namespace object created from command-line arguments. Must
    have the attributes 'extensions' and 'input'
    """
    msg =  "No files found with [" +', '.join(opts.extensions) + "] "
    msg += "extension" +("s " if len(opts.extensions) > 1 else " ")
    msg += "in " + opts.input
    # if recursive
    msg += " or any of its subdirectories"
    print(msg)


def print_modified_files(anchors):
    """
    Prints out which files were modified amongst those looked at

    :param anchors: Dictionary mapping file path strings to dictionaries
        containing AnchorHub tag/generated header key-value pairs
    """
    print("Files with modifications:")
    for file_path in anchors:
        print("  " + file_path)
    print("")


def print_summary_stats(counter):
    """
    Prints summary statistics about which writer strategies were used,
    and how much they were used.

    :param counter: A list of lists. The first entry on the inner list is a
        number count of how many times a WriterStrategy was used, and the
        second entry is a string label describing the WriterStrategy
    """
    sum = 0
    for c in counter:
        print("Total " + c[1] + " modified:\t" + str(c[0]))
        sum += c[0]
    print("total modifications: \t\t" + str(sum))
