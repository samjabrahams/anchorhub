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

##
## STANDARD LINK REGEX
##

anchor_link = r"\[.+\]\s*\(\s*[^\s\)]*#[^\s\)]+\s*\)"


##
## REFERENCE LINK REGEX
##

# Regex patterns for valid reference links
valid_reference_link = r"^ {0,3}\[.+\]:\s+\S*#\S+\s+(['\"]).+\1\s*$|^ {0,3}\[.+\]:\s+\S*#\S+\s+\(.+\)\s*$|^ {0,3}\[.+\]:\s+\S*#\S+\s*$"

# Regex that will match the beginning portion of a reference link pattern
# Note that this pattern, on its own, cannot ensure complete valid syntax
# Use the "Regex for complete valid reference link" patterns above for that
reference_link = r"^ {0,3}\[.+\]:\s+\S*#\S+"


##
## CODE BLOCK REGEX
##

# Regex for code-block demarcation
code_block_start = r"^```"
code_block_end = r"^```\s*$"


##
## HEADER REGEX
##

# Create regex for start/stop wrapper pattern based on open/closing wrappers
def make_wrapper(opn, close):
    return re.escape(opn) + r"\s*#((?!" + re.escape(opn) + r")(?!" + re.escape(close) +")\S)+\s*" + re.escape(close)

# Regex for marked atx header
def make_atx_header(wrapper_pattern):
    return r"^#+ .+" + wrapper_pattern + r"\s*$"

# Regex for Setext header/anchor line
def make_setext_header(wrapper_pattern):
    return r"^.+" + wrapper_pattern + r"\s*$" 

# Regex for Setext underline of a header
setext_underline = r"^([-=])\1*\s*$"


