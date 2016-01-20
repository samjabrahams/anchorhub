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

##
## Step 0: Import required modules and define required functions
##

import re
import sys
import os
import glob

# ## Define functions

# Given a string path to a file, returns the file name plus extension
def get_file_name_from_path(path):
	return path[path.rfind('/') + 1:]

# Given a directory path, returns the path string, making sure it ends with a forward slash '/'
def end_string_in_char(string, char):    
    if len(char) != 1:
        # Should throw some sort of error
        return string    
    if string[-1] != char:
        return string + char
    else:
        return string

def strip_relative_directories(path):
	index = path.rfind('./')
	return path[index+2:]

def esc_special_chars(word):
    out = ""
    for letter in word:
        if not re.match(r"\w", word):
            # Letter is a special character
            out += "\\" + letter
        else:
            # Letter is alphanumeric
            out += letter
    return out

def write_to_file(path, text):
    # Open file with read capabilties
    f = open(path, 'w')
            
    # Write text to file
    f.write(text)
            
    # Close the file
    f.close()

# Creates a new anchor link, constructed from the original text
# A header with the form "   This is my Cool Header!!" creates
# the anchor "#this-is-my-cool-header"
# arg: header - Header string to be converted to an anchor
# arg: existingHeaders - a list of anchors that is used to check
#		the newly constructed anchor. If an existing anchor matches, a
#		number (starting from 1) is concatenated to the end and it checks
#		for uniqueness again. This repeats with incrementing numbers until a
#		unique anchor tag is found
def create_anchor_from_header(header, existing_anchors=None, max_repeat=100):
    # Strip white space on the left/right and make lower case
    out = header.strip().lower()

    # Replace groups of white space with hyphens
    out = re.sub(r"\s+", lambda x: "-", out, flags=re.UNICODE)

    # Remove characters that aren't alphanumeric, hyphens, or spaces
    out = re.sub(r"[^\w\- ]+", lambda x: "", out, flags=re.UNICODE)

    if existing_anchors:
        if out in existing_anchors:
            i = 1
            while (out + "-" + str(i)) in existing_anchors and i <= max_repeat:
                i +=  1
                
            if i <= max_repeat:
                return out + "-" + str(i)
            else:
                # Throw some error
                print "Stop using the same header over and over again!!"
    
    return out

##
## Step 1: Define input/output directories, as well as #header indicators and overwrite flag
##

# Define the directory separators for either Unix or Windows systems
if os.name == 'nt':
    separator = '\\'
else:
    separator = '/'

# Root directory for search
# Default to '.'
IN_DIR = end_string_in_char('../test/in', separator)

# Output directory
OUT_DIR = end_string_in_char('../test/out', separator)

print "Root input directory: \t", IN_DIR
print "Outputting to: \t\t", OUT_DIR + "\r\n"

# Demarcation for start/stop of #header notation
# Default to {} braces
BOTH = '{ }'
BOTH_LIST = BOTH.split()

# Sanity check that there are exactly two patterns given to identify headers 
if len(BOTH_LIST) != 2:
    print "Header demarcation must be of the form \r\n\t'{startpattern} {stoppattern}'"
    print "(Note the space between the two patterns)"
    sys.exit()
    
OPEN = BOTH_LIST[0]
CLOSE = BOTH_LIST[1]

OVERWRITE = False

##
## Step 2: Find all file paths for Markdown files in subdirectories
##

# Get list of Markdown files in root directory and all subdirectories
file_paths = []
for root, _, _ in os.walk(IN_DIR):
    file_paths += glob.glob(root + separator + '*.md')

# Check in with user
print "Configuring the following Markdown files:"
for fl in file_paths:
    print "  ", fl
print

##
## Step 3: Find all marked headers in the files
##

# ## Define regex patterns

# Regex for start/stop wrapper pattern
wrapper_pattern = re.escape(OPEN) + r"\s*#((?!" + re.escape(OPEN) + r")(?!" + re.escape(CLOSE) +").)+\s*" + re.escape(CLOSE)
# Regex for marked header
header_pattern = "^#+ .+" + wrapper_pattern + "\s*$"

# Regex for local anchor links
local_anchor_link_pattern = r"\]\(#[^\)]+\)"

# Regex for external anchor links
external_anchor_link_pattern = r"\]\([^\)]+\.md#[^\)]+\)"

header_regex = re.compile(header_pattern, re.UNICODE)
wrapper_regex = re.compile(wrapper_pattern, re.UNICODE)
local_regex = re.compile(local_anchor_link_pattern, re.UNICODE)
external_regex = re.compile(external_anchor_link_pattern, re.UNICODE)

def find_last_match(regexObj, string):
    matches = regexObj.findall(string)
    return matches[len(matches) - 1]

# Storage for all header dictionary
# Stores sub-dictionaries for each file
headers = {}

# Count for headers, local links, and external links modified
modified_counts = [0,0,0]

for file_path in file_paths:
    # Local file headers to be placed in the global headers dict
    file_headers = {}
    
    # Open the file with read capabilities
    f = open(file_path, 'r')
    
    # Go through each line in the file
    for line in f:
        if header_regex.search(line):
            # Line has '# Header {#id}' format
            
            # Index of the start of the header, after '#' characters
            start_index = line.find('# ') + 2
            
            # Index of the start and end identifiers
            start_id_index = line.rfind(OPEN)
            end_id_index = line.rfind(CLOSE)
            
            header_id = line[start_id_index + len(OPEN) + 1:end_id_index]
            header_anchor = create_anchor_from_header(line[start_index:start_id_index], file_headers.values())
            
            file_headers[header_id] = header_anchor
    
    f.close()
    
    # Remove IN_DIR portion of file_path
    
    file_key = file_path[len(IN_DIR):]
    
    headers[file_key] = file_headers

##
## Step 4: Remove {#anchor} syntax and replace all relevent anchors with GitHub-style anchors
##

# Second pass through files
# Change lines of code that use or reference {#anchor} tags
for file_path in file_paths:
    
    # Get file_key by stripping out IN_DIR portion of file_path
    file_key = file_path[len(IN_DIR):]
    
    # 'modified_text' will be used to re-write the file 
    # Text from file will be copied line by line
    # changing specific portions as needed
    modified_text = ""
    
    # Boolean flag that is set to True if a line is changed
    file_is_modified = False
    
    # Open file with read capabilties
    f = open(file_path, 'r')
    
    for line in f:
        has_anchor_header = header_regex.search(line)
        has_local_anchor_link = local_regex.search(line)
        has_external_anchor_link = external_regex.search(line)
        
        if (has_anchor_header
            or has_local_anchor_link
            or has_external_anchor_link):
            
            # We need to modify this line
            
            # File will need to be rewritten later
            file_is_modified = True
            
            # Holder for modified line
            replacement_line = line
            
            if has_anchor_header:
                # Line has a header with {#anchor} notation
            
                # Index of the start of the braces notation
                open_brace_index = replacement_line.rfind(OPEN)
                
                # Use everything except for the {#anchor} tag
                replacement_line = replacement_line[:open_brace_index] + "\r\n"

                # Increment header modified count
                modified_counts[0] += 1
                
            if has_local_anchor_link:                
                # Line has at least one local anchor link
                
                # Holder for incremental changes to replacement_line
                # replacement_line will be replaced by this at the end of this section 
                changed_line = ""
                
                # Get list of all local link start and end indices
                links=[m.span() for m in local_regex.finditer(replacement_line)]
                
                # Most recent index used
                last_index = 0
                
                for link in links:
                    # Check each local header link and change if necessary
                    
                    link_start_index = link[0]
                    link_end_index = link[1]
                    
                    # Extract #anchor text
                    anchor = replacement_line[link_start_index + 3 : link_end_index - 1]
                    
                    if anchor in headers[file_key]:
                        # The anchor has been identified in {#anchor} notation before
                        # Replace the link with the corresponding GitHub style anchor
                        changed_line += replacement_line[last_index : link_start_index] + "](#" + headers[file_key][anchor] + ")"

                        # Increment local links modified count
                        modified_counts[1] += 1
                    else:
                        # Normal anchor: don't change it
                        changed_line += replacement_line[last_index : link_end_index]
                    
                    last_index = link_end_index
                    
                # Include the end of the line
                changed_line += replacement_line[last_index:]
                
                # Push changes to replacement_line
                replacement_line = changed_line
                
            if has_external_anchor_link:
                # Line has at least one external anchor link

                # Holder for incremental changes to replacement_line
                # replacement_line will be replaced by this at the end of this section 
                changed_line = ""
                
                # Get list of all link start and end indices
                links=[m.span() for m in external_regex.finditer(replacement_line)]
                
                # Most recent index used
                last_index = 0
                
                for link in links:
                    # Check each external header link and change if necessary
                    
                    # Start/end index of link text inside of replacement_line
                    link_start_index = link[0]
                    link_end_index = link[1]
                    
                    # The url of the link, with braces and parentheses removed
                    # link_start_index+2 to cut off '](' characters
                    # link_end_index-1 to cut off ')' character
                    link_text = replacement_line[link_start_index + 2:link_end_index - 1]
                    
                    # Sanity check: Make sure that the link doesn't go to an absolute path
                    if os.path.isabs(link_text):
                        print "Absolute path found."
                        continue
                    
                    # Index of the hash/pound sign
                    hash_index = link_text.rfind('.md#') + 3
                    
                    # Index of the hash/pound sign, relative to the whole replacement_line
                    abs_hash_index = hash_index + link_start_index + 2
                    
                    # Anchor text
                    anchor = link_text[hash_index + 1:]
                    
                    # Path to linked Markdown file, relative to current document
                    link_relative_path = link_text[:hash_index]
                    
                    link_key = os.path.relpath(IN_DIR + link_relative_path, IN_DIR)
                    
                    if link_key in headers and anchor in headers[link_key]:
                        # The anchor has been identified in {#anchor} notation before
                        # Replace the link with the corresponding GitHub style anchor
                        changed_line += replacement_line[last_index : abs_hash_index] + "#" + headers[link_key][anchor] + ")"

                        # Increment external links modified count
                        modified_counts[2] += 1
                    else:
                        # Normal anchor: don't change it
                        changed_line += replacement_line[last_index : link_end_index]
                    
                    last_index = link_end_index
                                                
                # Include the end of the line
                changed_line += replacement_line[last_index:]
                
                # Push changes to replacement_line
                replacement_line = changed_line
            
            # Add modified line to the text holder
            modified_text += replacement_line
            
        else:
            # Line does not need to be modified
            modified_text += line
    
    # Close the file!
    f.close()
    
    if OVERWRITE:
        # Re-write file to original location
        if file_is_modified:
            # Only write if file has changes
            write_to_file(file_path, modified_text)
            
    else:
        # Write file to OUT_DIR
        
        # Use same directory hierarchy inside of output directory
        final_destination = OUT_DIR + file_key
        
        # Ensure that directories in path to final_destination exist
        if not os.path.exists(os.path.dirname(final_destination)):
            os.makedirs(os.path.dirname(final_destination))
        
        write_to_file(final_destination, modified_text)

print "Total headers modified: \t" + str(modified_counts[0])
print "Total local links modified: \t" + str(modified_counts[1])
print "Total external links modified: \t" + str(modified_counts[2])
print "Total modifications: \t\t" + str(sum(modified_counts))
