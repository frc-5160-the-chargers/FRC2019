# hatch_mechanism.py
# code to operate the hatch mechanism on the front of kirkland

from wpilib import DoubleSolenoid

import enum

from Kirkland import robotmap


class HatchGrabberPositions(enum.Enum):
    GRABBING = enum.auto()
    RELEASED = enum.auto()


class HatchGrabber:
    hatch_grab_actuator: DoubleSolenoid

    def __init__(self):
        self.state = HatchGrabberPositions.RELEASED

    def grab(self):
        self.state = HatchGrabberPositions.GRABBING

    def release(self):
        self.state = HatchGrabberPositions.RELEASED

    def toggle(self):
        self.state = HatchGrabberPositions.RELEASED if self.state == HatchGrabberPositions.GRABBING else HatchGrabberPositions.GRABBING

    def execute(self):
        if self.state == HatchGrabberPositions.GRABBING:
            self.hatch_grab_actuator.set(
                robotmap.Tuning.HatchMechanism.Grabber.grabbing_state)
        if self.state == HatchGrabberPositions.RELEASED:
            self.hatch_grab_actuator.set(
                robotmap.Tuning.HatchMechanism.Grabber.released_state)


class HatchRackPositions(enum.Enum):
    EXTENDED = enum.auto()
    RETRACTED = enum.auto()


class HatchRack:
    hatch_rack_actuator_left: DoubleSolenoid
    hatch_rack_actuator_right: DoubleSolenoid

    def __init__(self):
        self.state = HatchRackPositions.RETRACTED

    def extend(self):
        self.state = HatchRackPositions.EXTENDED

    def retract(self):
        self.state = HatchRackPositions.RETRACTED

    def toggle(self):
        self.state = HatchRackPositions.EXTENDED if self.state == HatchRackPositions.RETRACTED else HatchRackPositions.RETRACTED

    def execute(self):
        if self.state == HatchRackPositions.EXTENDED:
            self.hatch_rack_actuator_left.set(
                robotmap.Tuning.HatchMechanism.Rack.extended_state)
            self.hatch_rack_actuator_right.set(
                robotmap.Tuning.HatchMechanism.Rack.extended_state)
        if self.state == HatchRackPositions.RETRACTED:
            self.hatch_rack_actuator_left.set(
                robotmap.Tuning.HatchMechanism.Rack.retracted_state)
            self.hatch_rack_actuator_right.set(
                robotmap.Tuning.HatchMechanism.Rack.retracted_state)


class HatchMechanismState(enum.Enum):
    RETRACTED_GRABBING = enum.auto()
    EXTENDED_GRABBING = enum.auto()
    EXTENDED_RELEASED = enum.auto()


class HatchMechanism:
    # tl;dr a questionable state machine
    hatch_grabber: HatchGrabber
    hatch_rack: HatchRack

    def __init__(self):
        self.state = HatchMechanismState.RETRACTED_GRABBING

    def extend(self):
        if self.state == HatchMechanismState.RETRACTED_GRABBING:
            self.state = HatchMechanismState.EXTENDED_GRABBING
            self.hatch_rack.extend()

    def retract(self):
        if self.state == HatchMechanismState.EXTENDED_GRABBING:
            self.state = HatchMechanismState.RETRACTED_GRABBING
            self.hatch_rack.retract()

    def grab(self):
        if self.state == HatchMechanismState.EXTENDED_RELEASED:
            self.state = HatchMechanismState.EXTENDED_GRABBING
            self.hatch_grabber.grab()

    def release(self):
        if self.state == HatchMechanismState.EXTENDED_GRABBING:
            self.state = HatchMechanismState.EXTENDED_RELEASED
            self.hatch_grabber.release()

    def execute(self):
        pass
