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

def main(argv=None):

    ##
    ## Import required modules and variables
    ##
    # Global modules
    import re
    import sys
    import os
    import glob
    import argparse

    # AnchorHub modules
    import anchor_functions as ahf
    from anchor_variables import separator, output_default, wrapper_default

    ##
    ## Step 0: Parse command line arguments
    ##
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(version="0.5", description="anchorhub parses through Markdown files and precompiles links to specially formatted anchors")

    parser.add_argument("input", help="Path of directory tree to be parsed")
    parser.add_argument("output", nargs='?', default=output_default, help="Desired output location (default is \"" + output_default + "\")")
    parser.add_argument("-X", "--overwrite", help="Overwrite input files, ignore output location", action="store_true")
    parser.add_argument("-e", "--extension", nargs="+", help="Indicate which file extensions to search and run anchorhub on.", default=[".md"])
    parser.add_argument("-w", "--wrapper", default=wrapper_default, help="Specify custom wrapper format (default is \"{ }\")")

    args = vars(parser.parse_args())

    ##
    ## Step 1: Define input/output directories, as well as #header wrapper and overwrite flag
    ##

    # Root directory for parsing
    IN_DIR = ahf.end_string_in_char(args['input'], separator)

    # Output directory
    OUT_DIR = ahf.end_string_in_char(args['output'], separator)

    # Demarcation for start/stop of #header notation
    # Default to { } braces
    WRAPPER = args['wrapper']
    WRAPPER_LIST = WRAPPER.split()

    # Sanity check that there are exactly two patterns given to identify headers 
    if len(WRAPPER_LIST) != 2:
        print("Error: Header demarcation must be of the form \r\n\t'{startpattern} {stoppattern}'")
        print("(Note the space between the two patterns)")
        sys.exit()
       
    OPEN = WRAPPER_LIST[0]
    CLOSE = WRAPPER_LIST[1]

    # Flag to say whether this program should overwrite the existing files instead of outputting to a different locations
    OVERWRITE = args['overwrite']

    # File extensions that the program will search for and perform processing on
    EXTENSIONS = args['extension']

    # Make sure that an empty string isn't specified as an extension type
    if "" in EXTENSIONS:
        print("ERROR: An empty string is not a valid extension.")
        sys.exit()

    # Make sure that the user hasn't specified the same input and output directories without using the overwrite flag
    if (os.path.abspath(IN_DIR) == os.path.abspath(OUT_DIR)) and not OVERWRITE:
        # User specified the same output directory as input directory, which would overwrite files!
        # We won't do that without them giving us the overwrite flag
        # Let's give the user a warnng and a suggestion
        print("WARNING: Input and output directories are the same, but --overwrite flag is not provided.\r\n")
        print("Do you want to overwrite your input files? If so, use the following command:")
        print("\tanchorhub -X " + args['input'])
        sys.exit()

    # Confirm the directories that will be processed 
    print("Root input directory: \t" + IN_DIR)
    print("Outputting to: \t\t" + OUT_DIR + "\r\n")

    ##
    ## Step 2: Find all file paths for Markdown files in subdirectories
    ##

    # Get list of Markdown files in root directory and all subdirectories
    file_paths = ahf.list_all_files_in_directory_with_extensions(IN_DIR, EXTENSIONS, exclude=OUT_DIR)

    if len(file_paths) < 1:
        # Didn't find any files to process
        print("No files found with [" + ', '.join(EXTENSIONS) + "] extension" + ("s" if len(EXTENSIONS) > 1 else "") + " in " + IN_DIR + " or any of its subdirectories.")
        sys.exit()

    # Check in with user about which files are going to be processed
    print("Configuring the following files:")
    for fl in file_paths:
        print("  " + fl)
    print("")
    
    ##
    ## Step 3: Find all marked headers in the files
    ##

    # ## Define regex patterns

    # Regex for start/stop wrapper pattern
    wrapper_pattern = re.escape(OPEN) + r"\s*#((?!" + re.escape(OPEN) + r")(?!" + re.escape(CLOSE) +")\S)+\s*" + re.escape(CLOSE)
    # Regex for marked header
    header_pattern = "^#+ .+" + wrapper_pattern + "\s*$"

    # Regex for local anchor links
    local_anchor_link_pattern = r"\[.+\]\(#[^\)]+\)"

    # Regex for external anchor links
    external_anchor_link_pattern = r"\[.+\]\([^\)]+\.md#[^\)]+\)"

    # Regex for code-block demarcation
    code_block_start_pattern = r"^```"
    code_block_end_pattern = r"^```\s*$"

    header_regex = re.compile(header_pattern, re.UNICODE)
    wrapper_regex = re.compile(wrapper_pattern, re.UNICODE)
    local_regex = re.compile(local_anchor_link_pattern, re.UNICODE)
    external_regex = re.compile(external_anchor_link_pattern, re.UNICODE)

    code_start_regex = re.compile(code_block_start_pattern, re.UNICODE)
    code_end_regex = re.compile(code_block_end_pattern, re.UNICODE)

    # Storage for all header dictionary
    # Stores sub-dictionaries for each file
    headers = {}

    # Count for headers, local links, and external links modified
    modified_counts = [0,0,0]

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
        f = open(file_path, 'r')

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
                    # The id has already been used- instruct user to modify their code.
                    print("ERROR: Duplicate anchor tags used.\r\n")
                    print("File: " + file_path + " line " + line_number)
                    print("The anchor tag " + header_id + " was already used for the previous header " + file_headers[header_id])
                    print("\r\nPlease modify your code to remove duplicates")
                    if not duplicate_headers[file_path]:
                        duplicate_headers[file_path] = []
                    duplicate_headers[file_path] += [header_id, line_number, file_headers[header_id]]

                file_headers[header_id] = header_anchor
        
            if (code_end_regex.search(line) and in_code_block and not already_switched):
                # This line marks the end of a ``` code block
                in_code_block = False

        f.close()
        
        # Remove IN_DIR portion of file_path
        
        file_key = file_path[len(IN_DIR):]
        
        headers[file_key] = file_headers

    ###
    ### END OF FIRST PASS THROUGH THE FILES
    ###

    # Check to see if there were any duplicate headers
    if len(duplicate_headers) > 0:
        # We have duplicate headers
        # Print out instructions to the user to remove duplicates and exit
        ahf.print_duplicate_header_information(duplicate_headers)

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

    for file_path in file_paths:
        
        # Get file_key by stripping out IN_DIR portion of file_path
        file_key = file_path[len(IN_DIR):]
        
        # 'modified_text' will be used to re-write the file 
        # Text from file will be copied line by line
        # changing specific portions as needed
        modified_text = ""
        
        # Boolean flag that is set to True if a line is changed
        file_is_modified = False

        # Boolean flag that keeps track of whether or not a ``` style code block is currently open
        in_code_block = False
        
        # Open file with read capabilties
        f = open(file_path, 'r')
        
        for line in f:
            has_anchor_header = header_regex.search(line)
            has_local_anchor_link = local_regex.search(line)
            has_external_anchor_link = external_regex.search(line)

            # Flag to make sure we don't flip twice on the same line
            already_switched = False

            if (code_start_regex.search(line) and not in_code_block):
                # This line represents the start of a ``` code block
                in_code_block = True
                already_switched = True

            
            if (not in_code_block and
                (has_anchor_header
                or has_local_anchor_link
                or has_external_anchor_link)):
                
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
                        
                        # Index of the '](#' characters in the link
                        url_begin = replacement_line[link_start_index:link_end_index].find('](#')

                        # Extract #anchor text
                        anchor = replacement_line[link_start_index + url_begin + 3 : link_end_index - 1]

                        print(anchor)
                        
                        if anchor in headers[file_key]:
                            # The anchor has been identified in {#anchor} notation before
                            # Replace the link with the corresponding GitHub style anchor
                            changed_line += replacement_line[last_index : link_start_index + url_begin] + "](#" + headers[file_key][anchor] + ")"

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

                        # Regex match object for ]( (with no escaping backslash preceding it)
                        braces_match = re.search(r"[^\\]\]\(",replacement_line[link_start_index:link_end_index], flags=re.UNICODE)
                        # Index of where the link ends ](
                        braces_index = braces_match.end()

                        # The url of the link, with braces and parentheses removed
                        # link_start_index+2 to cut off '](' characters
                        # link_end_index-1 to cut off ')' character
                        link_text = replacement_line[link_start_index + braces_index:link_end_index - 1]

                        print(braces_index)
                        print(link_text)

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
                        
                        print(link_key)

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

            if (code_end_regex.search(line) and in_code_block and not already_switched):
                # This line marks the end of a ``` code block
                in_code_block = False
        
        # Close the file!
        f.close()
        
        if OVERWRITE:
            # Re-write file to original location
            if file_is_modified:
                # Only write if file has changes
                ahf.write_to_file(file_path, modified_text)
                
        else:
            # Write file to OUT_DIR
            
            # Use same directory hierarchy inside of output directory
            final_destination = OUT_DIR + file_key
            
            # Ensure that directories in path to final_destination exist
            if not os.path.exists(os.path.dirname(final_destination)):
                os.makedirs(os.path.dirname(final_destination))
            
            ahf.write_to_file(final_destination, modified_text)

    ###
    ### END OF SECOND PASS THROUGH FILES
    ###

    print("Total headers modified: \t" + str(modified_counts[0]))
    print("Total local links modified: \t" + str(modified_counts[1]))
    print("Total external links modified: \t" + str(modified_counts[2]))
    print("Total modifications: \t\t" + str(sum(modified_counts)))

if __name__ == "__main__":
    main()