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
    f = open(path, 'wb')
            
    # Write text to file
    f.write(text)
            
    # Close the file
    f.close()

def find_last_match(regexObj, string):
    matches = regexObj.findall(string)
    return matches[len(matches) - 1]