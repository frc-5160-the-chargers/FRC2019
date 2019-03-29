from wpilib import Servo
import enum

class CargoServoPosition(enum.Enum):
    LOCKED = enum.auto()
    UNLOCKED = enum.auto()

class CargoServo:
    locked_position = 180
    unlocked_position = 0

    cargo_servo_rotator : Servo

    def __init__(self):
        self.current_position = CargoServoPosition.LOCKED

    def lock(self):
        self.current_position = CargoServoPosition.UNLOCKED
    
    def unlock(self):
        self.current_position = CargoServoPosition.LOCKED

    def toggle_lock(self):
        self.current_position = CargoServoPosition.UNLOCKED if self.current_position == CargoServoPosition.LOCKED else CargoServoPosition.LOCKED

    def execute(self):
        self.cargo_servo_rotator.setAngle(CargoServo.locked_position if self.current_position == CargoServoPosition.LOCKED else CargoServo.unlocked_position)