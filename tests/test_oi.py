import pytest
import OI

def test_add_two(control, fake_time, robot):
    value = robot.get_oi().add_two()
    assert value == 4