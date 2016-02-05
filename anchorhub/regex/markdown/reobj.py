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
import patterns as p
from anchorhub.core.lazyregex import LazyRegex

class MarkdownRegex(object):
    def __init__(self, opn, close):
        self._opn = opn
        self._close = close
        self._wrapper_pattern = p.make_wrapper(opn, close)
        self._wrapper_regex = re.compile(self._wrapper_pattern, re.UNICODE)

        # Define LazyRegex objects to hold patterns
        self._atx = LazyRegex(p.make_atx_header(self._wrapper_pattern))
        self._setext_header = LazyRegex(p.make_setext_header(self._wrapper_pattern))
        self._setext_underline = LazyRegex(p.setext_underline)

        # Define LazyRegex for reference link patterns
        self._validref = LazyRegex(p.valid_reference_link)
        self._reference = LazyRegex(p.reference_link)

        # Define LazyRegex for code blocks
        self._code_start = LazyRegex(p.code_block_start)
        self._code_end = LazyRegex(p.code_block_end)


    ##### ATX REGEX

    def atx_test(self, this_line, next_line):
        return self._atx.match(this_line)

    def get_atx_regex(self):
        return self._atx.get_regex()

    #####

    ##### SETEXT REGEX

    # Helper test that automatically checks for both a line with a wrapper
    # Immediately followed by a valid "underline"
    def setext_test(self, this_line, next_line):
        return (self._setext_header.match(this_line) and 
            self._setext_underline.match(next_line) )

    def get_setext_header_regex(self):
        return self._setext_header.get_regex()

    def get_setext_underline_regex(self):
        return self._setext_underline.get_regex()

    #####

    ##### REFERENCE LINK REGEX

    def valid_ref_test(self, this_line, next_line):
        return self._validref.match(this_line)

    def get_reference_regex(self):
        return self._reference.get_regex()

    #####

    ##### CODE BLOCK REGEX
    def code_start_test(self, this_line, next_line):
        return self._code_start.match(this_line)

    def code_end_test(self, this_line, next_line):
        return self._code_end.match(this_line)