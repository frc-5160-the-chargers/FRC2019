# cargo_mechanism.py
# the code to run the cargo mechanism on the back of Kirkland

from ctre import WPI_TalonSRX
from wpilib import Servo

import enum

import robotmap
from utils import clamp


class CargoRotator:
    # TODO make sure that this motor is configured so that positive power raises it
    cargo_mechanism_motor_rotator: WPI_TalonSRX

    def __init__(self):
        self.power = 0
        self.enabled = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def raise_bucket(self, power):
        self.power = power

    def lower_bucket(self, power):
        # NOTE: expects a positive power!
        self.power = -power

    def execute(self):
        if self.enabled:
            motor_power = clamp(self.power, -robotmap.Tuning.CargoMechanism.Rotator.lowering_power_limit,
                                robotmap.Tuning.CargoMechanism.Rotator.lifting_power_limit)
            self.cargo_mechanism_motor_rotator.set(motor_power)
        else:
            self.cargo_mechanism_motor_rotator.stopMotor()


class CargoServoPosition(enum.Enum):
    LOCKED = enum.auto()
    UNLOCKED = enum.auto()


class CargoServo:
    cargo_mechanism_servo_lock: Servo

    def __init__(self):
        self.current_position = CargoServoPosition.LOCKED

    def lock(self):
        self.current_position = CargoServoPosition.LOCKED

    def unlock(self):
        self.current_position = CargoServoPosition.UNLOCKED

    def toggle_lock(self):
        self.current_position = CargoServoPosition.LOCKED if self.current_position == CargoServoPosition.UNLOCKED else CargoServoPosition.UNLOCKED

    def get_locked(self):
        return self.current_position == CargoServoPosition.LOCKED

    def execute(self):
        degrees = robotmap.Tuning.CargoMechanism.Servo.locked_position if self.current_position == CargoServoPosition.LOCKED else robotmap.Tuning.CargoMechanism.Servo.unlocked_position
        self.cargo_mechanism_servo_lock.setAngle(degrees)


class CargoMechanism:
    cargo_rotator: CargoRotator
    cargo_locking_servo: CargoServo

    def __init__(self):
        pass

    def toggle_lock(self):
        self.cargo_locking_servo.toggle_lock()
        if self.cargo_locking_servo.get_locked():
            self.cargo_rotator.disable()
        else:
            self.cargo_rotator.enable()

    def raise_lift(self, power):
        if self.cargo_locking_servo.get_locked():
            return
        self.cargo_rotator.raise_bucket(power)

    def lower_lift(self, power):
        if self.cargo_locking_servo.get_locked():
            return
        self.cargo_rotator.lower_bucket(power)

    def execute(self):
        pass

    def reset(self):
        self.cargo_locking_servo.lock()
        self.cargo_rotator.disable()
