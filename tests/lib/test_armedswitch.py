"""
Tests for the ArmedSwitch class

ArmedSwitch:
http://www.github.com/samjabrahams/anchorhub/lib/armedswitch.py
"""
from anchorhub.lib.armedswitch import ArmedSwitch


def test_init_base():
    """
    Test basic initalization state
    :return:
    """
    s = ArmedSwitch()
    assert s.is_switched() == False
    assert s.is_armed() == True

def test_init_values():
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
    Test for basic switch() functionality
    :return:
    """
    s = ArmedSwitch()
    assert s.is_switched() == False
    s.switch()
    assert s.is_switched() == True
    assert s.is_armed() == False

def test_switch_only_once():
    """
    Make sure switch doesn't change twice without re-arming it
    :return:
    """
    s = ArmedSwitch()
    assert s.is_switched() == False
    s.switch()
    s.switch()
    assert s.is_switched() == True

def test_switch_only_once_loop():
    """
    Attempt to flip switch 100 times
    Make sure it only ever switches once
    :return:
    """
    s = ArmedSwitch()
    assert s.is_switched() == False
    for i in range(0,99):
        s.switch()
        assert s.is_switched() == True

def test_switch_argument():
    """
    Makes sure switch() arguments work as intended
    :return:
    """
    s1 = ArmedSwitch()
    s1.switch(False)
    assert s1.is_switched() == False
    assert s1.is_armed() == False

    s2 = ArmedSwitch()
    s2.switch(True)
    assert s2.is_switched() == True
    assert s2.is_armed() == False

def test_arm():
    """
    Makes sure that arm() works
    :return:
    """
    s = ArmedSwitch()
    s.switch()
    assert s.is_armed() == False
    s.arm()
    assert s.is_armed() == True
    s.switch()
    assert s.is_switched() == False
    assert s.is_armed() == False

def test_disarm():
    """
    Makes sure disarm() works
    :return:
    """
    s = ArmedSwitch()
    s.disarm()
    assert s.is_armed() == False