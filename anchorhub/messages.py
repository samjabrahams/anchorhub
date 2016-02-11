"""
messages.py - Functions that print out messages to the console
"""


def print_directories(opts):
    """
    Prints the input and output directories to the console.

    :param opts: namespace that contains printable 'input' and 'output' fields.
    """
    print("Root input directory: \t" + opts.input)
    print("Outputting to: \t\t" + opts.output + "\r\n")
