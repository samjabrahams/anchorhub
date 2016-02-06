"""
Tests for the ArmedCheckSwitch class

ArmedCheckSwitch:
http://www.github.com/samjabrahams/anchorhub/lib/armedcheckswitch.py
"""

from anchorhub.lib.armedcheckswitch import ArmedCheckSwitch


def test_init_base():
    """
    Test basic functionality and default parameters of ArmedCheckSwitch init
    :return:
    """
    s = ArmedCheckSwitch()
    assert s.is_switched() == False
    assert s.is_armed() == True


def test_init_params():
    """
    Test initializing ArmedCheckSwitch with different starting values
    :return:
    """
    s1 = ArmedCheckSwitch(switched=True, armed=False)
    assert s1.is_switched() == True
    assert s1.is_armed() == False

    s2 = ArmedCheckSwitch(switched=False, armed=False)
    assert s2.is_switched() == False
    assert s2.is_armed() == False

    s3 = ArmedCheckSwitch(armed=True, switched=True)
    assert s3.is_switched() == True
    assert s3.is_armed() == True

    s4 = ArmedCheckSwitch(armed=True, switched=False)
    assert s4.is_switched() == False
    assert s4.is_armed() == True


def is_equal_to_one(n):
    """
    Simple function to use as a callback for tests
    :param n: Integer. Compared to 1
    :return:
    """
    return n == 1


def is_equal_to_two(n):
    """
    Simple function to use as a callback for tests
    :param n: Integer. Compared to 2
    :return:
    """
    return n == 2


def test_switch():
    """
    Test ArmedCheckSwitch.switch()
    :return:
    """
    s = ArmedCheckSwitch(on_check=is_equal_to_one, off_check=is_equal_to_two)
    assert s.is_switched() == False

    assert s.switch(n=4) == False
    assert s.is_switched() == False

    assert s.switch(n=1) == True
    assert s.is_switched() == True

    # Should need to re-arm before switching again
    assert s.switch(n=2) == False
    assert s.is_switched() == True

    s.arm()
    assert s.switch(n=2) == True
    assert s.is_switched() == False


def test_switch_on_off():
    """
    Test ArmedCheckSwitch.switch_on() and ArmedCheckSwitch.switch_off()
    :return:
    """
    s = ArmedCheckSwitch(on_check=is_equal_to_one, off_check=is_equal_to_two)
    assert s.is_switched() == False

    assert s.switch_on(n=3) == False
    assert s.is_switched() == False

    assert s.switch_on(n=1) == True
    assert s.is_switched() == True

    assert s.switch_off(n=1) == False
    assert s.is_switched() == True

    # Should need to re-arm the switch to turn it off
    assert s.switch_off(n=2) == False
    assert s.is_switched() == True

    s.arm()
    assert s.switch_off(n=2) == True
    assert s.is_switched() == False


def test_arm():
    """
    Test ArmedCheckSwitch.arm()
    :return:
    """
    s = ArmedCheckSwitch()
    assert s.is_armed() == True
    assert s.switch() == True
    assert s.is_armed() == False
    s.arm()
    assert s.is_armed() == True


def test_disarm():
    """
    Test ArmedCheckSwitch.disarm()
    :return:
    """
    s = ArmedCheckSwitch()
    assert s.is_armed() == True
    s.disarm()
    assert s.is_armed() == False
