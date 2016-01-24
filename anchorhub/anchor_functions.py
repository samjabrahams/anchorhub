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

import re
import os
import glob

from anchor_variables import separator

# ## Define functions

# Given a directory path, returns the path string, making sure it ends with a forward slash '/'
def end_string_in_char(string, char):    
    if len(char) != 1:
        # Should throw some sort of error
        return string    
    if string[-1] != char:
        return string + char
    else:
        return string

# Helper method to quickly output text to a given file path
def write_to_file(path, text):
    # Open file with read capabilties
    f = open(path, 'w')
            
    # Write text to file
    f.write(text)
            
    # Close the file
    f.close()

def find_last_match(regexObj, string):
    matches = regexObj.findall(string)
    return matches[len(matches) - 1]

# Creates a new anchor link, constructed from the original text
# A header with the form "   This is my Cool Header!!" creates
# the anchor "#this-is-my-cool-header"
# arg: header - Header string to be converted to an anchor
# arg: existingHeaders - a list of anchors that is used to check
#		the newly constructed anchor. If an existing anchor matches, a
#		number (starting from 1) is concatenated to the end and it checks
#		for uniqueness again. This repeats with incrementing numbers until a
#		unique anchor tag is found
def create_anchor_from_header(header, existing_anchors=None):
    # Strip white space on the left/right and make lower case
    out = header.strip().lower()

    # Replace groups of white space with hyphens
    out = re.sub(r"\s+", lambda x: "-", out, flags=re.UNICODE)

    # Remove characters that aren't alphanumeric, hyphens, or spaces
    out = re.sub(r"[^\w\- ]+", lambda x: "", out, flags=re.UNICODE)

    if existing_anchors:
        if out in existing_anchors:
            i = 1
            while (out + "-" + str(i)) in existing_anchors:
                i +=  1
            return out + "-" + str(i)
    
    return out

# Get list of all files with given extention in root directory and all subdirectories
# Do not include files in 'exclude' directory
def list_all_files_in_directory_with_extensions(dir, exts, exclude):
    file_paths = []
    for root, _, _ in os.walk(dir):
        for ext in exts:
            file_paths+= glob.glob(root + separator + '*' + ext)

    if exclude is not None:
        # Make sure that Markdown files within the OUT_DIR are not modified
        paths_to_remove = []

        for file_path in file_paths:
            if os.path.commonprefix([file_path, exclude]) is exclude:
                paths_to_remove.append(file_path)

        for path in paths_to_remove:
            file_paths.remove(path)

    return file_paths

# Display instructions to user on how to fix duplicate anchor tags
def print_duplicate_header_information(duplicates):
    print("ERROR: Duplicate anchors specified on the same page(s)")
    print("Please modify your code to remove duplicates.\r\n")
    for file_path in duplicates:
        for line_info in duplicates[file_path]:
            print("File: " + file_path + " line " + line_info[1])
            print("\t Anchor " + line_info[0] + " already used for previous header: " + line_info[2])
