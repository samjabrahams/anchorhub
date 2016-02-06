"""
Class file for the ArmedSwitch class
"""
class ArmedSwitch(object):
    """
    ArmedSwitch is a boolean switch that must be explicitly re-armed after
    each time it switches, or else it keeps the same state.
    """

    # __init__: ArmedSwitch initializer
    def __init__(self, switched=False, armed=True):
        """
        Initializer for ArmedSwitch. Default switched state is False,
        and ready-to-be switched state set to True
        :param switched: Boolean. Starting state of the switch
        :param armed: Boolean. Starting state of the armed property. When False,
        the switch must be re-armed with the arm() method before switching
        again
        :return:
        """
        self._switched = switched
        self._armed = armed

    def switch(self, val=None):
        """
        Set the state of the switch. If the armed state is set to False,
        the function does nothing
        :param val: Boolean. The value to set the switch state to. When None,
        the switch will be set to the opposite of its current state.
        :return:
        """
        if self._armed:
            if val == None:
                val = not self._switched
            self._switched = val
            self._armed = False

    def arm(self):
        """
        Sets the armed state of the switch to True
        :return:
        """
        self._armed = True

    def disarm(self):
        """
        Sets the armed state of the switch to False
        :return:
        """
        self._armed = False

    def is_switched(self):
        """
        Returns the current state of the switch
        :return: Boolean
        """
        return self._switched

    def is_armed(self):
        """
        Returns the currened armed status of the switch
        :return: Boolean
        """
        return self._armed