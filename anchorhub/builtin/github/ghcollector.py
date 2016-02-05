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

from anchorhub.core.collector import AnchorCollector, AnchorCollectorStrategy
from anchorhub.core.switches.testarmedswitch import TestArmedSwitch
from anchorhub.regex.markdown.reobj import MarkdownRegex
import header_transform as ht

def getCollector(opn, close):

    mdrx = MarkdownRegex(opn, close)

    class MarkdownAtxCollectorStrategy(AnchorCollectorStrategy):
        
        def __init__(self):
            pass

        def test(self, this_line, next_line):
            return mdrx.atx_test(this_line, next_line)

        def get(self, this_line, next_line, file_anchors):
            # Line has '# Header {#id}' format
            # Index of the start of the header, after '#' characters
            start_index = this_line.find('# ') + 2

            # Index of the start and end identifiers
            start_anchor = this_line.rfind(opn)
            end_anchor = this_line.rfind(close)
            
            anchor = this_line[start_anchor + len(opn) + 1:end_anchor]

            header = this_line[start_index:start_anchor]

            return anchor, header

    atx = MarkdownAtxCollectorStrategy()

    code_block_switch = TestArmedSwitch(on_test=mdrx.code_start_test, off_test=mdrx.code_end_test)

    return AnchorCollector(ht.create_anchor_from_header, [atx], switches=[code_block_switch])
