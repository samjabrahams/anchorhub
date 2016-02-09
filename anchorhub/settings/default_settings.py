"""
Defaults for all settings used by AnchorHub
"""

WRAPPER = '{ }'

INPUT = '.'
OUTPUT = 'out-anchorhub'

ARGPARSER = {
    'description': "anchorhub parses through Markdown files and precompiles "
                   "links to specially formatted anchors."
}
ARGPARSE_INPUT = {
    'help': "Path of directory tree to be parsed",
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
    'default': [".md"]
}
ARGPARSE_WRAPPER = {
    'help': "Specify custom wrapper format (default is \"" + WRAPPER + "\")",
    'default': WRAPPER
}
