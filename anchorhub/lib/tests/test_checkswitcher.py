"""
Tests for the ArmedCheckSwitch class

ArmedCheckSwitch:
http://www.github.com/samjabrahams/anchorhub/lib/armedcheckswitch.py
"""

from anchorhub.lib.armedcheckswitch import ArmedCheckSwitch


def test_init_base():
    """
    armedcheckswitch.py: Test __init__() and its default parameters
    """
    s = ArmedCheckSwitch()
    assert s.is_switched() == False
    assert s.is_armed() == True


def test_init_params():
    """
    armedcheckswitch.py: Test __init__() with different parameters
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
    :return: True if n equals 1. False otherwise
    """
    return n == 1


def is_equal_to_two(n):
    """
    Simple function to use as a callback for tests
    :param n: Integer. Compared to 2
    :return: True if n equals 2. False otherwise
    """
    return n == 2


def test_switch():
    """
    armedcheckswitch.py: Test switch()
    """
    s = ArmedCheckSwitch(on_check=is_equal_to_one, off_check=is_equal_to_two)
    assert s.is_switched() == False

    assert s.switch(4) == False
    assert s.is_switched() == False

    assert s.switch(1) == True
    assert s.is_switched() == True

    # Should need to re-arm before switching again
    assert s.switch(2) == False
    assert s.is_switched() == True

    s.arm()
    assert s.switch(2) == True
    assert s.is_switched() == False


def test_switch_on_off():
    """
    armedcheckswitch.py: Test switch_on() and switch_off()
    """
    s = ArmedCheckSwitch(on_check=is_equal_to_one, off_check=is_equal_to_two)
    assert s.is_switched() == False

    assert s.switch_on(3) == False
    assert s.is_switched() == False

    assert s.switch_on(1) == True
    assert s.is_switched() == True

    assert s.switch_off(1) == False
    assert s.is_switched() == True

    # Should need to re-arm the switch to turn it off
    assert s.switch_off(2) == False
    assert s.is_switched() == True

    s.arm()
    assert s.switch_off(2) == True
    assert s.is_switched() == False


def test_arm():
    """
    armedcheckswitch.py: Test arm()
    """
    s = ArmedCheckSwitch()
    assert s.is_armed() == True
    assert s.switch() == True
    assert s.is_armed() == False
    s.arm()
    assert s.is_armed() == True


def test_disarm():
    """
    armedcheckswitch.py: Test disarm()
    """
    s = ArmedCheckSwitch()
    assert s.is_armed() == True
    s.disarm()
    assert s.is_armed() == False
