"""
Tests for the ArmedSwitch class

ArmedSwitch:
http://www.github.com/samjabrahams/anchorhub/lib/armedswitch.py
"""
from anchorhub.lib.armedswitch import ArmedSwitch


def test_init_base():
    """
    lib/armedswitch.py: Test basic initialization state
    """
    s = ArmedSwitch()
    assert s.is_switched() == False
    assert s.is_armed() == True


def test_init_params():
    """
    lib/armedswitch.py: Test initializing with different starting values
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
    lib/armedswitch.py: Test basic switch() functionality
    """
    s = ArmedSwitch()
    assert s.is_switched() == False
    assert s.switch() == True
    assert s.is_switched() == True
    assert s.is_armed() == False


def test_switch_only_once():
    """
    lib/armedswitch.py: Ensure doesn't change twice without re-arming
    """
    s = ArmedSwitch()
    assert s.is_switched() == False
    assert s.switch() == True
    assert s.switch() == False
    assert s.is_switched() == True


def test_switch_only_once_loop():
    """
    lib/armedswitch.py: ensure only switches once during a loop of 100 attempts
    """
    s = ArmedSwitch()
    assert s.is_switched() == False
    assert s.switch() == True
    for i in range(0,99):
        assert s.switch() == False
        assert s.is_switched() == True


def test_switch_argument():
    """
    lib/armedswitch.py: Makes sure switch() arguments work as intended
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
    lib/armedswitch.py: Test arm()
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
    lib/armedswitch.py: Test disarm()
    """
    s = ArmedSwitch()
    s.disarm()
    assert s.is_armed() == False
