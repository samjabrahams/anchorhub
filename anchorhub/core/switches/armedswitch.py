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

# ArmedSwitch is a switch that must be re-armed before it can switch again
# It is useful for situations where a switch may be triggered by multiple tests in a loop
# But should only be flipped once per loop cycle
#
# Typical code use:
# ```
# as = new ArmedSwitch()
# if (test):
#     as.switch()
# if (test2):
#     as.switch()
# ...
# if (testN):
#     as.switch()
# print(as.is_switched())    # will return True if ANY tests are successful
# ...
# # Re-arm the switch
# as.arm()    # Ready to switch again
# ```
class ArmedSwitch(object):

    # __init__: ArmedSwitch initializer
    def __init__(self, switched=False, armed=True):     
        self._switched = switched
        self._armed = armed

    def switch(self, val=None):
        if val == None:
            val = not self._switched
        if self._armed:
            self._switched = val
            self._armed = False

    def arm(self):
        self._armed = True

    def is_switched(self):
        return self._switched

    def is_armed(self):
        return self._armed