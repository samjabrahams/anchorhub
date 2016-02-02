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
# Regex for local anchor links
local_anchor_link_pattern = r"\[.+\]\(#[^\)]+\)"

# Regex for external anchor links
external_anchor_link_pattern = r"\[.+\]\([^\)]+\.md#[^\)]+\)"


##
## REFERENCE LINK REGEX
##

# Regex patterns for valid reference links
# A valid reference link line will match one of the following patterns
#
# Regex for complete valid reference link with double quote wrapped title
valid_reference_link_pattern_double_quote =r'^ {0,3}\[.+\]:\s+\S*#\S+\s+".+"\s*$'
# Regex for complete valid reference link with single quote wrapped title
valid_reference_link_pattern_single_quote =r"^ {0,3}\[.+\]:\s+\S*#\S+\s+'.+'\s*$"
# Regex for complete valid reference link with parentheses wrapped title
valid_reference_link_pattern_parentheses =r"^ {0,3}\[.+\]:\s+\S*#\S+\s+(.+)\s*$"
# Regex for complete valid reference link with no title
valid_reference_link_pattern_notitle =r"^ {0,3}\[.+\]:\s+\S*#\S+\s*$"

# Regex that will match the beginning portion of a reference link pattern
# Note that this pattern, on its own, cannot ensure complete valid syntax
# Use the "Regex for complete valid reference link" patterns above for that
reference_link_pattern = r"^ {0,3}\[.+\]:\s+\S*#\S+"


##
## CODE BLOCK REGEX
##

# Regex for code-block demarcation
code_block_start_pattern = r"^```"
code_block_end_pattern = r"^```\s*$"


##
## HEADER REGEX
##

# Create regex for start/stop wrapper pattern based on open/closing wrappers
def make_wrapper_pattern(open, close):
    return re.escape(open) + r"\s*#((?!" + re.escape(open) + r")(?!" + re.escape(close) +")\S)+\s*" + re.escape(close)

# Regex for marked atx header
def make_atx_header_pattern(wrapper_pattern):
    return r"^#+ .+" + wrapper_pattern + r"\s*$"

# Regex for Setext header/anchor line
def make_settext_header_pattern(wrapper_pattern):
    return r"^.+" + wrapper_pattern + r"\s*$" 

# Regex for Setext underline of a header
settext_underline_pattern = r"^([-=])\1*\s*$"

def make_


