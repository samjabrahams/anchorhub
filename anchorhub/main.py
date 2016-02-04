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

def main():

    ##
    ## Import required modules and variables
    ##
    # Global modules
    import re
    import sys
    import os
    import glob
    import argparse
    from os import path

    # AnchorHub modules
    import anchor_functions as ahf
    import messages
    import helpers
    import cmdparse
    import anchor_regex as ahr
    from anchor_variables import separator, output_default, wrapper_default

    ##
    ## Step 0: Parse command line arguments
    ##
    args = cmdparse.parse_args()

    ##
    ## Step 1: Define input/output directories, as well as #header wrapper and overwrite flag
    ##

    IN_DIR, OUT_DIR, OPEN, CLOSE, OVERWRITE, EXTENSIONS = cmdparse.get_options(args)

    # Confirm the directories that will be processed 
    print("Root input directory: \t" + IN_DIR)
    print("Outputting to: \t\t" + OUT_DIR + "\r\n")

    ##
    ## Step 2: Find all file paths for Markdown files in subdirectories
    ##

    # Get list of Markdown files in root directory and all subdirectories
    file_paths = ahf.list_all_files_in_directory_with_extensions(IN_DIR, EXTENSIONS, exclude=OUT_DIR)
    ahf.strip_prefix_from_list(file_paths, IN_DIR)
    
    if len(file_paths) < 1:
        # Didn't find any files to process
        messages.print_no_files_found(EXTENSIONS, IN_DIR)
        sys.exit()

    # Check in with user about which files are going to be processed
    print("Parsing the following files:")
    for file_path in file_paths:
        print("  " + file_path)
    print("")
    
    ##
    ## Step 3: Find all marked headers in the files
    ##

    # ## Define regex patterns

    # Regex for start/stop wrapper pattern
    wrapper_pattern = re.escape(OPEN) + r"\s*#((?!" + re.escape(OPEN) + r")(?!" + re.escape(CLOSE) + r")\S)+\s*" + re.escape(CLOSE)
    # Regex for marked header
    header_pattern = r"^#+ .+" + wrapper_pattern + r"\s*$"

    # Regex for local anchor links
    local_anchor_link_pattern = r"\[.+\]\(#[^\)]+\)"

    # Regex for external anchor links
    external_anchor_link_pattern = r"\[.+\]\([^\)]+\.md#[^\)]+\)"
    
    # Regex for reference links
    reference_link_pattern = r"^ {0,3}\[.+\]:\s+\S*#\S+"

    # Regex for code-block demarcation
    code_block_start_pattern = r"^```"
    code_block_end_pattern = r"^```\s*$"

    header_regex = re.compile(header_pattern, re.UNICODE)
    wrapper_regex = re.compile(wrapper_pattern, re.UNICODE)
    local_regex = re.compile(local_anchor_link_pattern, re.UNICODE)
    external_regex = re.compile(external_anchor_link_pattern, re.UNICODE)
    reference_regex = re.compile(reference_link_pattern, re.UNICODE)

    link_regex = re.compile(r"\[.+\]\s*\(\s*[^\s\)]*#[^\s\)]+\s*\)", re.UNICODE)

    code_start_regex = re.compile(code_block_start_pattern, re.UNICODE)
    code_end_regex = re.compile(code_block_end_pattern, re.UNICODE)

    # Storage for all header dictionary
    # Stores sub-dictionaries for each file
    headers = {}

    ###
    ### FIRST PASS THROUGH THE FILES
    ### FIND ALL OF THE HEADERS THAT USE THE SPECIFIED WRAPPER SYNTAX
    ###

    # Dictionary to hold duplicate header values, if any
    # If any are found after the pass, we will exit the program and let the user know where the duplicates are
    duplicate_headers = {}

    for file_path in file_paths:
        # Local file headers to be placed in the global headers dict
        file_headers = {}
        
        # Open the file with read capabilities
        f = open(file_path, 'rb')

        # Boolean flag that keeps track of whether or not a ``` style code block is currently open
        in_code_block = False
        
        # Go through each line in the file
        for line_number, line in enumerate(f, 1):

            # Flag to make sure we don't flip twice on the same line
            already_switched = False

            if (code_start_regex.search(line) and not in_code_block):
                # This line represents the start of a ``` code block
                in_code_block = True
                already_switched = True

            if (code_end_regex.search(line) and in_code_block and not already_switched):
                # This line marks the end of a ``` code block
                in_code_block = False

            if header_regex.search(line) and not in_code_block:
                # Line has '# Header {#id}' format
                
                # Index of the start of the header, after '#' characters
                start_index = line.find('# ') + 2
                
                # Index of the start and end identifiers
                start_id_index = line.rfind(OPEN)
                end_id_index = line.rfind(CLOSE)
                
                header_id = line[start_id_index + len(OPEN) + 1:end_id_index]
                header_anchor = ahf.create_anchor_from_header(line[start_index:start_id_index], file_headers.values())
                
                # Check to make sure that the id hasn't been used already
                if header_id in file_headers:
                    # The id has already been used- place it in the duplicate_headers dict
                    # Will instruct users on fixing this afterward
                    if not duplicate_headers[file_path]:
                        duplicate_headers[file_path] = []
                    duplicate_headers[file_path] += [header_id, line_number, file_headers[header_id]]

                file_headers[header_id] = header_anchor
        
        f.close()
        
        headers[file_path] = file_headers

    ###
    ### END OF FIRST PASS THROUGH THE FILES
    ###

    # Check to see if there were any duplicate anchors
    if len(duplicate_headers) > 0:
        # We have duplicate headers
        # Print out instructions to the user to remove duplicates and exit
        messages.print_duplicate_anchor_information(duplicate_headers)

    ##
    ## Step 4: Remove {#anchor} syntax and replace all relevent anchors with GitHub-style anchors
    ##

    ###
    ### SECOND PASS THROUGH FILES
    ### 
    ### CHANGE LINES OF CODE THAT:
    ###     - ARE HEADERS THAT HAVE THE SPECIFIED WRAPPER SYNTAX
    ###     - HAVE LINKS THAT REFERENCE SPECIFIED ANCHORS ON THE SAME PAGE
    ###     - HAVE LINKS THAT REFERENCE SPECIFIED ANCHORS ON OTHER PAGES
    ### 
    ### THEN OUTPUT THOSE CHANGES TO THE GIVEN OUTPUT DIRECTORY USING THE
    ### SAME STRUCTURE AS THE INPUT DIRECTORY
    ###

    # Count for headers, local links, and external links modified
    modified_counts = [0,0,0,0]

    ####
    # IN THE FUTURE, WE'D IDEALLY LIKE TO NOT REWRITE FILES THAT DON'T REQUIRE MODIFICATIONS
    ####

    for file_path in file_paths:
        
        # 'modified_text' will be used to re-write the file 
        # Text from file will be copied line by line
        # changing specific portions as needed
        modified_text = ""
        
        # Boolean flag that is set to True if a line is changed
        file_is_modified = False

        # Boolean flag that keeps track of whether or not a ``` style code block is currently open
        in_code_block = False
        
        # Open file with read capabilties
        f = open(file_path, 'rb')
        
        for line in f:
            has_anchor_header = header_regex.search(line)
            has_local_anchor_link = local_regex.search(line)
            has_external_anchor_link = external_regex.search(line)
            has_reference_link = reference_regex.search(line)
            has_anchor_link = link_regex.search(line)

            # Flag to make sure we don't flip twice on the same line
            already_switched = False

            if (code_start_regex.search(line) and not in_code_block):
                # This line represents the start of a ``` code block
                in_code_block = True
                already_switched = True

            if (code_end_regex.search(line) and in_code_block and not already_switched):
                # This line marks the end of a ``` code block
                in_code_block = False
            
            if (not in_code_block and
                (has_anchor_header
                or has_local_anchor_link
                or has_anchor_link
                or has_external_anchor_link)
                or has_reference_link):
                
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
                    replacement_line = replacement_line[:open_brace_index - 1] + "\r\n"

                    # Increment header modified count
                    modified_counts[0] += 1
                
                if has_anchor_link:
                    # Line has at least one inline link with an anchor tag in it

                    # Holder for incremental changes to replacement_line
                    # replacement_line will be replaced by this at the end of this section 
                    changed_line = ""

                    links = [m.span() for m in link_regex.finditer(replacement_line)]

                    # Most recent index used
                    last_index = 0

                    for link in links:
                        # Check each link and change if necessary
                        link_start_index = link[0]
                        link_end_index = link[1]

                        link_text = replacement_line[link_start_index:link_end_index]

                        url_start = re.search(r"\[.+\]\s*\(", link_text).end()

                        url_text = link_text[url_start:len(link_text) - 1].strip()

                        print("URL IS '" + url_text + "'")

                        hash_index = url_text.find('#')

                        link_file = url_text[:hash_index]

                        anchor = url_text[hash_index + 1:]

                        if link_file == "":
                            link_key = file_path

                        else:
                            link_key = os.path.relpath(IN_DIR + os.path.dirname(file_path) + separator + link_file, IN_DIR)

                        print("Key: " + link_key)
                        print("Anchor: " + anchor)

                        if link_key in headers and anchor in headers[link_key]:
                            # The anchor has been identified in {#anchor} notation before
                            # Replace the link with the corresponding GitHub style anchor

                            changed_line += replacement_line[last_index: link_start_index + url_start] + link_file + "#" + headers[link_key][anchor] + ")"

                            if link_file == "":
                                # Increment local inline link counter
                                modified_counts[1] += 1
                            else:
                                # Increment external inline link counter
                                modified_counts[2] += 1

                        else:
                            # Normal anchor: don't change it
                            changed_line += replacement_line[last_index : link_end_index]

                        last_index = link_end_index

                    # Include the end of the line
                    changed_line += replacement_line[last_index:]

                    # Push changes to replacement_line
                    replacement_line = changed_line

                if has_local_anchor_link and False:                
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
                        
                        # Index of the '](#' characters in the link
                        url_begin = replacement_line[link_start_index:link_end_index].find('](#')

                        # Extract #anchor text
                        anchor = replacement_line[link_start_index + url_begin + 3 : link_end_index - 1]
                        
                        if anchor in headers[file_path]:
                            # The anchor has been identified in {#anchor} notation before
                            # Replace the link with the corresponding GitHub style anchor
                            changed_line += replacement_line[last_index : link_start_index + url_begin] + "](#" + headers[file_path][anchor] + ")"

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
                    
                if has_external_anchor_link and False:
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

                        # Regex match object for ]( (with no escaping backslash preceding it)
                        braces_match = re.search(r"[^\\]\]\(",replacement_line[link_start_index:link_end_index], flags=re.UNICODE)
                        # Index of where the link ends ](
                        braces_index = braces_match.end()

                        # The url of the link, with braces and parentheses removed
                        # link_start_index+2 to cut off '](' characters
                        # link_end_index-1 to cut off ')' character
                        link_text = replacement_line[link_start_index + braces_index:link_end_index - 1]

                        # Sanity check: Make sure that the link doesn't go to an absolute path
                        if os.path.isabs(link_text):
                            print("Absolute path found.")
                            continue
                        
                        # Index of the hash/pound sign
                        hash_index = link_text.rfind('.md#') + 3
                        
                        # Index of the hash/pound sign, relative to the whole replacement_line
                        abs_hash_index = hash_index + link_start_index + braces_index
                        
                        # Anchor text
                        anchor = link_text[hash_index + 1:]
                        
                        # Path to linked Markdown file, relative to current document
                        link_relative_path = link_text[:hash_index]
                        
                        # The key for the referenced file in the headers dictionary, if such a key has been made
                        link_key = os.path.relpath(IN_DIR + os.path.dirname(file_path) + separator + link_relative_path, IN_DIR)

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

                if has_reference_link and ahr.is_valid_reference_link(line):
                    # Line is a local reference link

                    # MatchObject for the link
                    link = reference_regex.match(replacement_line)

                    link_start_index = replacement_line.find(']:') + 2
                    link_end_index = link.end()

                    link_text = replacement_line[link_start_index:link_end_index].strip()

                    hash_index = link_text.find('#')

                    link_file = link_text[:hash_index]

                    anchor = link_text[hash_index + 1:]

                    if link_file == "":
                        link_key = file_path

                    else: 
                        link_key = os.path.relpath(IN_DIR + os.path.dirname(file_path) + separator + link_file, IN_DIR)

                    if link_key in headers and anchor in headers[link_key]:
                        # The anchor has been identified in {#anchor} notation before
                        # Replace the link with the corresponding GitHub style anchor

                        replacement_line = replacement_line[0:link_start_index] + " " + link_file + "#" + headers[link_key][anchor] + replacement_line[link_end_index:]

                        modified_counts[3] += 1
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
                helpers.write_to_file(file_path, modified_text)
                
        else:
            # Write file to OUT_DIR
            
            # Use same directory hierarchy inside of output directory
            final_destination = OUT_DIR + file_path
            
            # Ensure that directories in path to final_destination exist
            if not os.path.exists(os.path.dirname(final_destination)):
                os.makedirs(os.path.dirname(final_destination))
            
            helpers.write_to_file(final_destination, modified_text)

    ###
    ### END OF SECOND PASS THROUGH FILES
    ###

    messages.print_modified_files(headers)

    messages.print_summary_stats(modified_counts)

if __name__ == "__main__":
    main()