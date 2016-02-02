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

# Display instructions to user on how to fix duplicate anchor tags
def print_duplicate_anchor_information(duplicates):
    print("ERROR: Duplicate anchors specified on the same page(s)")
    print("Please modify your code to remove duplicates.\r\n")
    for file_path in duplicates:
        for line_info in duplicates[file_path]:
            print("File: " + file_path + " line " + line_info[1])
            print("\t Anchor " + line_info[0] + " already used for previous header: " + line_info[2])

# Print out that there no files were found with given extensions
def print_no_files_found(extensions, in_dir):
    print("No files found with [" + ', '.join(extensions) + "] extension" + ("s" if len(extensions) > 1 else "") + " in " + in_dir + " or any of its subdirectories.")

def print_modified_files(headers):
    print("Files with modifications:")
    for file_path in headers:
        print("  " + file_path)
    print("")

def print_summary_stats(modified_counts):
    print("Total headers modified: \t" + str(modified_counts[0]))
    print("Total local links modified: \t" + str(modified_counts[1]))
    print("Total external links modified: \t" + str(modified_counts[2]))
    print("Total reference links modified: " + str(modified_counts[3]))
    print("Total modifications: \t\t" + str(sum(modified_counts)))
