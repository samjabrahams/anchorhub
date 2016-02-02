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

# Regex for complete valid reference link with double quote wrapped title
valid_reference_link_pattern_double_quote =r'^ {0,3}\[.+\]:\s+\S*#\S+\s+".+"\s*$'
# Regex for complete valid reference link with single quote wrapped title
valid_reference_link_pattern_single_quote =r"^ {0,3}\[.+\]:\s+\S*#\S+\s+'.+'\s*$"
# Regex for complete valid reference link with parentheses wrapped title
valid_reference_link_pattern_parentheses =r"^ {0,3}\[.+\]:\s+\S*#\S+\s+(.+)\s*$"
# Regex for complete valid reference link with no title
valid_reference_link_pattern_notitle =r"^ {0,3}\[.+\]:\s+\S*#\S+\s*$"

valid_ref_double_regex = re.compile(valid_reference_link_pattern_double_quote, re.UNICODE)
valid_ref_single_regex = re.compile(valid_reference_link_pattern_single_quote, re.UNICODE)
valid_ref_paren_regex = re.compile(valid_reference_link_pattern_parentheses, re.UNICODE)
valid_ref_notitle_regex = re.compile(valid_reference_link_pattern_notitle, re.UNICODE)

def is_valid_reference_link(string):
    return (valid_ref_double_regex.match(string) or valid_ref_single_regex.match(string)
        or valid_ref_paren_regex.match(string) or valid_ref_notitle_regex.match(string) )
