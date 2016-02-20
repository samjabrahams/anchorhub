"""
Class file for ArmedCheckSwitcher
"""
from anchorhub.lib.armedswitch import ArmedSwitch


class ArmedCheckSwitch(object):
    """
    CheckSwitcher wraps an ArmedSwitch and its commands, allowing the user to
    define custom checks for both switching on and switching off. The switch
    will not change to its on or off state unless the corresponding check
    returns True.

    ArmedSwitch:
    http://www.github.com/samjabrahams/anchorhub/lib/armedswitch.py
    """

    def __init__(self, switched=False, armed=True, on_check=lambda: True,
                 off_check=lambda: True):
        """
        Initialization for the ArmedCheckSwitcher class. Instantiates the
        local ArmedSwitch object. Assigns user defined functions on_check and
        off_check to local variables. They both default to lambdas that always
        return True (equivalent to just having using the underlining
        ArmedSwitch object).

        :param switched: Boolean. Sets the initial state of the switch
        :param armed: Boolean. Sets the initial armed state of the switch
        :param on_check: A callback function that returns a Boolean, and takes
            in a dictionary as its parameter. The switch cannot change to the True
            state unless this function returns True.
        :param off_check: Callback function. Similar to on_check(), prevents
            the switch from changing to False unless the this returns True
        """
        self._switch = ArmedSwitch(switched=switched, armed=armed)
        self.on_check = on_check
        self.off_check = off_check

    def switch(self, *args):
        """
        Method that attempts to change the switch to the opposite of its
        current state. Calls either switch_on() or switch_off() to accomplish
        this.

        :param kwargs: an variable length dictionary of key-pair arguments
            passed through to either switch_on() or switch_off()
        :return: Boolean. Returns True if the switch changes state
        """
        if self.is_switched():
            return self.switch_off(*args)
        else:
            return self.switch_on(*args)

    def switch_on(self, *args):
        """
        Sets the state of the switch to True if on_check() returns True,
        given the arguments provided in kwargs.

        :param kwargs: variable length dictionary of key-pair arguments
        :return: Boolean. Returns True if the operation is successful
        """
        if self.on_check(*args):
            return self._switch.switch(True)
        else:
            return False

    def switch_off(self, *args):
        """
        Sets the state of the switch to False if off_check() returns True,
        given the arguments provided in kwargs.

        :param kwargs: variable length dictionary of key-pair arguments
        :return: Boolean. Returns True if the operation is successful
        """
        if self.off_check(*args):
            return self._switch.switch(False)
        else:
            return False

    def arm(self):
        """
        Arms the switch, allowing it to change state (if not already armed)
        """
        self._switch.arm()

    def disarm(self):
        """
        Disarms the switch, preventing it from changing state.
        """
        self._switch.disarm()

    def is_switched(self):
        """
        Returns the current state of the switch

        :return: Boolean. True if the switch's state is True
        """
        return self._switch.is_switched()

    def is_armed(self):
        """
        Returns the switch's current armed state

        :return: Boolean. True if the switch's armed state is True
        """
        return self._switch.is_armed()

    def force(self, state):
        """
        Forces the switch to be switched to a particular state, regardless of
        its armed status.

        :param state: Boolean value to set the switch to
        """
        self._switch.force(state)
