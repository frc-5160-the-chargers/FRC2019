import math
from enum import Enum, unique, auto
import json
import os

import wpilib

@unique
class Side(Enum):
    LEFT = auto()
    RIGHT = auto()

class OI:
    DEADZONE = 0.1

    def __init__(self):
        self.settings = {}
        
        self.beastMode = False
        self.twoStickMode = False

        self.driver_joystick = wpilib.XboxController(0)
        self.sysop_joystick = wpilib.XboxController(1)

   
    def getButtonPressed(self, controller : wpilib.XboxController, button):
        """
        Get button pressed on a given controller, but do it so that the config file can be used
            param self
            param controller: the wpilib.XboxController object to get button data from
            param button: the desired button to check, determined from the config file
        """
        return controller.getRawButtonPressed(button)
        
    def curve(self, i):
        return math.pow(i, 3)/1.25

    def deadzone(self, i):
        if i < -OI.DEADZONE:
            return i
        elif i > OI.DEADZONE:
            return i
        else:
            return 0

    def process_input(self, joystick_input):
        return self.deadzone(self.curve(joystick_input) * (-1 if self.beastMode else 1))
    
    def process_driver_input(self, robot_side):
        if self.twoStickMode:
            if robot_side == Side.LEFT:
                return self.process_input(self.driver_joystick.getRawAxis(5 if self.beastMode else 1))
            elif robot_side == Side.RIGHT:
                return self.process_input(self.driver_joystick.getRawAxis(1 if self.beastMode else 5))
        else:
            if robot_side == Side.LEFT:
                return self.process_input(self.driver_joystick.getRawAxis(1))
            elif robot_side == Side.RIGHT:
                return -self.driver_joystick.getRawAxis(4)*0.7
    
    def drive_one_foot(self):
        return self.getButtonPressed(self.driver_joystick, self.settings["drive_foot"])

    def drivetrain_shifting_control(self):
        return self.getButtonPressed(self.driver_joystick, self.settings["drivetrain_shift"])

    def hatch_extend_control(self):
        return self.sysop_joystick.getRawButtonPressed(self.settings["hatch_extend"])
    
    def hatch_grab_control(self):
        return self.sysop_joystick.getRawButtonPressed(self.settings["hatch_grab"])

    def process_cargo_control(self):
        i = (self.sysop_joystick.getRawAxis(1)**3)/2
        if abs(self.sysop_joystick.getRawAxis(1)) > 0.1:
            return i
        else:
            return 0