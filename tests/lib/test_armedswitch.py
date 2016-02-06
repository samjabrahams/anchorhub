"""
Tests for the ArmedSwitch class

ArmedSwitch:
http://www.github.com/samjabrahams/anchorhub/lib/armedswitch.py
"""
from anchorhub.lib.armedswitch import ArmedSwitch


def test_init_base():
    """
    Test basic initialization state
    :return:
    """
    s = ArmedSwitch()
    assert s.is_switched() == False
    assert s.is_armed() == True


def test_init_params():
    """
    Test initializing ArmedSwitch with different starting values
    :return:
    """
    s1 = ArmedSwitch(switched=True, armed=False)
    assert s1.is_switched() == True
    assert s1.is_armed() == False

    s2 = ArmedSwitch(switched=False, armed=False)
    assert s2.is_switched() == False
    assert s2.is_armed() == False

    s3 = ArmedSwitch(armed=True, switched=True)
    assert s3.is_switched() == True
    assert s3.is_armed() == True

    s4 = ArmedSwitch(armed=True, switched=False)
    assert s4.is_switched() == False
    assert s4.is_armed() == True


def test_switch_basic():
    """
    Test basic ArmedSwitch.switch() functionality
    :return:
    """
    s = ArmedSwitch()
    assert s.is_switched() == False
    assert s.switch() == True
    assert s.is_switched() == True
    assert s.is_armed() == False


def test_switch_only_once():
    """
    Make ArmedSwitch doesn't change twice without re-arming it
    :return:
    """
    s = ArmedSwitch()
    assert s.is_switched() == False
    assert s.switch() == True
    assert s.switch() == False
    assert s.is_switched() == True


def test_switch_only_once_loop():
    """
    ArmedSwitch only switches once during a loop of 100 attempts
    :return:
    """
    s = ArmedSwitch()
    assert s.is_switched() == False
    assert s.switch() == True
    for i in range(0,99):
        assert s.switch() == False
        assert s.is_switched() == True


def test_switch_argument():
    """
    Makes sure ArmedSwitch.switch() arguments work as intended
    :return:
    """
    s1 = ArmedSwitch()
    assert s1.switch(False) == True
    assert s1.is_switched() == False
    assert s1.is_armed() == False

    s2 = ArmedSwitch()
    assert s2.switch(True) == True
    assert s2.is_switched() == True
    assert s2.is_armed() == False


def test_arm():
    """
    Test ArmedSwitch.arm()
    :return:
    """
    s = ArmedSwitch()
    assert s.switch() == True
    assert s.is_armed() == False
    s.arm()
    assert s.is_armed() == True
    assert s.switch() == True
    assert s.is_switched() == False
    assert s.is_armed() == False


def test_disarm():
    """
    Test ArmedSwitch.disarm()
    :return:
    """
    s = ArmedSwitch()
    s.disarm()
    assert s.is_armed() == False
