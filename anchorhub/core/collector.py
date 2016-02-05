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
from abc import ABCMeta, abstractmethod

class AnchorCollector(object):

    # convert(header, anchors=None): function that takes in a string and an optional
    #       dictionary of anchors
    def __init__(self, convert, strategies, switches=None):
        self._convert = convert
        self._strategies = strategies
        self._switches = switches

    # Returns anchor, header: the defined anchor tag and converted header (to autogenerated style)
    # Useds conver
    def collect(self, file_paths):
        anchors = {}
        duplicate_anchors = {}

        for file_path in file_paths:
            # Local file anchors to be placed in global anchors dict
            file_anchors = {}

            # Open the file with read capabilities
            f = open(file_path, 'rb')

            this_line = f.next()
            next_line = ""

            line_number = 1

            for line in f:
                next_line = line

                self._parseAnchorHeader(this_line, next_line, file_path, anchors, duplicate_anchors, file_anchors, line_number)

                this_line = next_line
                line_number += 1

            self._parseAnchorHeader(this_line, "", file_path, anchors, duplicate_anchors, file_anchors, line_number)
            f.close()

            anchors[file_path] = file_anchors

        return anchors, duplicate_anchors

    def _parseAnchorHeader(self, this_line, next_line, file_path, anchors, duplicate_anchors, file_anchors, line_number):
        for s in self._switches:
            s.switch(this_line, next_line)

        if not any(s.is_switched() for s in self._switches):
            for strategy in self._strategies:
                if strategy.test(this_line, next_line):
                    anchor, header = strategy.get(this_line, next_line, file_anchors)

                    if anchor in file_anchors:
                        # This anchor has been declared previously in the file
                        # Place in dublicate_anchors dictionary
                        # Instruct users on how to fix this afterward
                        if file_path not in duplicate_anchors:
                            # Instantiate dictionary entry under file_path if it has not been already
                            duplicate_anchors[file_path] = []
                        duplicate_anchors[file_path] += [header, line_number, file_anchors[anchor]]

                    converted_header = self._convert(header, file_anchors)
                    file_anchors[anchor] = converted_header

class AnchorCollectorStrategy(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    # Returns true if the line should be parsed with the get method
    @abstractmethod
    def test(self, this_line, next_line):
        pass

    # Should return the collected anchor, as well as the header portion that needs to be converted
    @abstractmethod
    def get(self, this_line, next_line, file_anchors):
        pass