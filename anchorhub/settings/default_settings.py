"""
Defaults for all settings used by AnchorHub
"""

WRAPPER = '{ }'

INPUT = '.'
OUTPUT = 'anchorhub-out'

ARGPARSER = {
    'description': "anchorhub parses through Markdown files and precompiles "
                   "links to specially formatted anchors."
}
ARGPARSE_INPUT = {
    'help': "Path of file or directory to parse",
}
ARGPARSE_OUTPUT = {
    'help': "Desired output location (default is \"" + OUTPUT + "\")",
    'default': OUTPUT
}
ARGPARSE_OVERWRITE = {
    'help': "Overwrite input files; ignore output location"
}
ARGPARSE_EXTENSION = {
    'help': "Indicate which file extensions to search and run anchorhub on.",
    'default': ['.md', '.markdown']
}
ARGPARSE_WRAPPER = {
    'help': "Specify custom wrapper format (default is \"" + WRAPPER + "\")",
    'default': WRAPPER
}
ARGPARSE_VERBOSE = {
    'help': "Generate verbose output with summary stats"
}
ARGPARSE_RECURSIVE = {
    'help': "Perform AnchorHub in the file hierarchy rooted with the input "
            "argument. AnchorHub tags are maintained across the file hierarchy"
}