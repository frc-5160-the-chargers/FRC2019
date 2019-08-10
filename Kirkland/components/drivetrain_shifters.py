# drivetrain_shifters.py
# code to run the shifters attached to the shifting gearboxes on the drivetrain

from wpilib import DoubleSolenoid

import enum

from Kirkland import robotmap


class ShifterGear(enum.Enum):
    LOW_GEAR = enum.auto()
    HIGH_GEAR = enum.auto()


class Shifters:
    left_shifter_actuator: DoubleSolenoid
    right_shifter_actuator: DoubleSolenoid

    def __init__(self):
        # NOTE: make sure that the robot is forced into low gear at the start of a match
        self.gear = ShifterGear.LOW_GEAR

    def shift_up(self):
        self.gear = ShifterGear.HIGH_GEAR

    def shift_down(self):
        self.gear = ShifterGear.LOW_GEAR

    def toggle(self):
        self.gear = ShifterGear.LOW_GEAR if self.gear == ShifterGear.HIGH_GEAR else ShifterGear.HIGH_GEAR

    def execute(self):
        if self.gear == ShifterGear.LOW_GEAR:
            self.left_shifter_actuator.set(
                robotmap.Tuning.Drivetrain.Shifters.low_gear_state)
            self.right_shifter_actuator.set(
                robotmap.Tuning.Drivetrain.Shifters.low_gear_state)

        if self.gear == ShifterGear.HIGH_GEAR:
            self.left_shifter_actuator.set(
                robotmap.Tuning.Drivetrain.Shifters.high_gear_state)
            self.right_shifter_actuator.set(
                robotmap.Tuning.Drivetrain.Shifters.high_gear_state)
