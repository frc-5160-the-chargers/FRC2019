import math
from enum import Enum, unique, auto

import wpilib

@unique
class Side(Enum):
    LEFT = auto()
    RIGHT = auto()

class OI:
    DEADZONE = 0.1

    def __init__(self):
        
        self.beastMode = False
        self.twoStickMode = False

        self.driver_joystick = wpilib.XboxController(0)

    def curve(self, i):
        return math.pow(i, 3)/1.25

    def deadzone(self, i):
        if i < -OI.DEADZONE:
            return i
        elif i > OI.DEADZONE:
            return i
        else:
            return 0

    def __process(self, joystick: wpilib.XboxController):
        return self.deadzone(self.curve(joystick) * (-1 if self.beastMode else 1))
    
    def process_driver_input(self, robot_side):
        if self.twoStickMode:
            if robot_side == Side.LEFT:
                return self.__process(self.driver_joystick.getRawAxis(5 if self.beastMode else 1))
            elif robot_side == Side.RIGHT:
                return self.__process(self.driver_joystick.getRawAxis(1 if self.beastMode else 5))
        else:
            if robot_side == Side.LEFT:
                return self.__process(self.driver_joystick.getRawAxis(1))
            elif robot_side == Side.RIGHT:
                return -self.driver_joystick.getRawAxis(4)/2
