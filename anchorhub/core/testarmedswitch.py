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

from switches.armedswitch import ArmedSwitch

class TestArmedSwitch(object):

    def __init__(self, on_test=lambda x, y: True, off_test=lambda x, y: True):     
        self.on_test = on_test
        self.off_test = off_test
        self._switch = ArmedSwitch()

    def switch(self, this_line, next_line):
        if self.is_switched():
            self.switch_off(this_line, next_line)
        else:
            self.switch_on(this_line, next_line)

    def switch_on(self, this_line, next_line):
        if self.on_test(this_line, next_line):
            self._switch.switch(True)

    def switch_off(self, this_line, next_line):
        if self.off_test(this_line, next_line):
            self._switch.switch(False)

    def arm(self):
        self._switch.arm()

    def is_switched(self):
        return self._switch.is_switched()

    def is_armed(self):
        return self._switch.is_armed()
