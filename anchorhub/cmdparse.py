# Copyright 2016, Sam Abrahams. All rights reserved.
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
# ==============================================================================

# Global modules
import argparse
import sys
import os
from os import path

# AnchorHub modules
import helpers
from anchor_variables import separator, output_default, wrapper_default

def parse_args():
    #with open(path.join(path.dirname(__file__), 'VERSION'), 'rb') as f:
    #    version = f.read().decode('ascii').strip()

    version = "0.12"

    parser = argparse.ArgumentParser(version=version, description="anchorhub parses through Markdown files and precompiles links to specially formatted anchors")

    parser.add_argument("input", help="Path of directory tree to be parsed")
    parser.add_argument("output", nargs='?', default=output_default, help="Desired output location (default is \"" + output_default + "\")")
    parser.add_argument("-X", "--overwrite", help="Overwrite input files, ignore output location", action="store_true")
    parser.add_argument("-e", "--extension", nargs="+", help="Indicate which file extensions to search and run anchorhub on.", default=[".md"])
    parser.add_argument("-w", "--wrapper", default=wrapper_default, help="Specify custom wrapper format (default is \"{ }\")")

    return vars(parser.parse_args())

# Checks to make sure that there are exactly two items in a list, otherwise exit
def check_wrapper(wrapper_list):
    if len(wrapper_list) != 2:
        print("Error: Header demarcation must be of the form \r\n\t'{startpattern} {stoppattern}'")
        print("(Note the space between the two patterns)")
        sys.exit()

# Checks to make sure there are no empty string extensions given
def check_extensions(extensions):
    # Make sure that an empty string isn't specified as an extension type
    if "" in extensions:
        print("ERROR: An empty string is not a valid extension.")
        sys.exit()

# If overwrite flag is not set to true
# checks to make sure that the input and output directories are not the same
# Else exits
def check_overwrite(in_dir, out_dir, overwrite):    
    if (not overwrite and os.path.abspath(in_dir) == os.path.abspath(out_dir)):
        # User specified the same output directory as input directory, which would overwrite files!
        # We won't do that without them giving us the overwrite flag
        # Let's give the user a warnng and a suggestion
        print("WARNING: Input and output directories are the same, but --overwrite flag is not provided.\r\n")
        print("Do you want to overwrite your input files? If so, use the following command:")
        print("\tanchorhub -X " + args['input'])
        sys.exit()

def get_options(args):
    # Root directory for parsing
    in_dir = helpers.end_string_in_char(args['input'], separator)

    # Output directory
    out_dir = helpers.end_string_in_char(args['output'], separator)

    # Flag to say whether this program should overwrite the existing files instead of outputting to a different locations
    overwrite = args['overwrite']

    # Make sure that the user hasn't specified the same input and output directories without using the overwrite flag
    check_overwrite(in_dir, out_dir, overwrite)

    # Demarcation for start/stop of #header notation
    # Default to { } braces
    wrapper = args['wrapper']
    wrapper_list = wrapper.split()

    # Sanity check that there are exactly two patterns given to identify headers 
    check_wrapper(wrapper_list)
       
    open_wrapper = wrapper_list[0]
    close_wrapper = wrapper_list[1]

    # File extensions that the program will search for and perform processing on
    extensions = args['extension']
    check_extensions(extensions)

    return in_dir, out_dir, open_wrapper, close_wrapper, overwrite, extensions

