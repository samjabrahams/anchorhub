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

class LazyRegex(object):
    def __init__(self, pattern):
        self._pattern = pattern

    def search(self, line):
        self._create_regex_if_none()
        return self._regex.search(line)

    def match(self, line):
        self._create_regex_if_none()
        return self._regex.match(line)

    def get_regex():
        self._create_regex_if_none()
        return self._regex

    def get_pattern():
        return self._pattern

    def _create_regex_if_none(self):
        if not hasattr(self, '_regex'):
            self._regex = re.compile(self._pattern, re.UNICODE)