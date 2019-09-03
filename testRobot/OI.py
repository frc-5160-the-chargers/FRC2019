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
    # TODO: determine if we even need this
    SETTINGSFILE = os.path.dirname(os.path.realpath(__file__)) + "/driverSettings.json"

    DEADZONE = 0.1

    def __init__(self):
        self.settings = {}

        self.arcade_drive = True
        self.beast_mode_active = False

        self.driver_joystick = wpilib.XboxController(0)
        self.sysop_joystick = wpilib.XboxController(1)

    #This method is no longer used but is kept so that the json file can be regenerated if necessary.
    @staticmethod
    def write_user_settings():
        # TODO: Note that in the future it might be better to put these into arrays so that we can have multiple buttons bound to one control -- just use *in* to check
        settings = {
            # sysop
            "hatch_grab" : wpilib.XboxController.Button.kB,
            "hatch_extend" : wpilib.XboxController.Button.kY,
            "hatch_autoretrieve" : wpilib.XboxController.Button.kX,
            "hatch_autoplace" : wpilib.XboxController.Button.kA,
            "calibrate_pressure_1" : wpilib.XboxController.Button.kStickLeft,
            "calibrate_pressure_2" : wpilib.XboxController.Button.kStickRight,

            # driver
            "drivetrain_shift" : wpilib.XboxController.Button.kBumperRight,
            "beast_mode" : wpilib.XboxController.Button.kA,
            "arcade_tank_shift" : wpilib.XboxController.Button.kX,
            "switch_main_camera" : wpilib.XboxController.Button.kB,
            "driver_override" : wpilib.XboxController.Button.kY
        }

        with open(OI.SETTINGSFILE, 'w') as outfile:
            json.dump(settings, outfile)

    def load_user_settings(self):
        with open(OI.SETTINGSFILE) as json_file:
            settings_dict = json.load(json_file)
            self.settings = settings_dict

    def get_button_pressed(self, controller : wpilib.XboxController, button):
        """
        Get button pressed on a given controller, but do it so that the config file can be used
            param self
            param controller: the wpilib.XboxController object to get button data from
            param button: the desired button to check, determined from the config file
        """
        return controller.getRawButtonPressed(button)

    def get_button_pressed_config(self, controller : wpilib.XboxController, button_name):
        """get button pressed using the names from the config file"""
        return self.get_button_pressed(controller, self.settings[button_name])
        
    def curve(self, i):
        """curve controller stick input"""
        return math.pow(i, 3)/1.25

    def deadzone(self, i):
        """see if input is within deadzone"""
        if i < -OI.DEADZONE:
            return i
        elif i > OI.DEADZONE:
            return i
        else:
            return 0

    def process_input(self, joystick_input):
        """apply deadzone and curving to input"""
        # TODO: consider applying beast mode later
        return self.deadzone(self.curve(joystick_input))
    
    def process_driver_input(self, robot_side):
        """handle driver input depending on the side passed in"""
        left_stick = 1
        right_stick = 5
        right_stick_x = 4

        turn_speed_modifier = 1.7       # yes this is that parameter that will need to be tuned every match because picky drivers

        if not self.arcade_drive:       # tank drive
            if robot_side == Side.LEFT:
                return self.process_input(self.driver_joystick.getRawAxis(left_stick))
            elif robot_side == Side.RIGHT:
                return self.process_input(self.driver_joystick.getRawAxis(right_stick))
        else:                           # arcade drive
            if robot_side == Side.LEFT:
                return self.process_input(self.driver_joystick.getRawAxis(left_stick))
            elif robot_side == Side.RIGHT:
                return -self.driver_joystick.getRawAxis(right_stick_x)/turn_speed_modifier
    

    # functions for checking individual buttons

    def process_cargo_control(self):
        """get output for the cargo grabber with curving"""
        i = self.curve(self.deadzone(self.sysop_joystick.getRawAxis(1))) # 1 is the left stick y axis
        return i
    
    def calibrate_pressure_sensor(self):
        """check and see if the pressure sensor needs to be calibrated"""
        return self.get_button_pressed_config(self.sysop_joystick, "calibrate_pressure_1") and self.get_button_pressed_config(self.sysop_joystick, "calibrate_pressure_2")
    
    def switch_cameras(self):
        return self.get_button_pressed_config(self.driver_joystick, "switch_main_camera")

    def grab_hatch(self):
        return self.get_button_pressed_config(self.sysop_joystick, "hatch_grab")

    def extend_hatch(self):
        return self.get_button_pressed_config(self.sysop_joystick, "hatch_extend")
        
    def auto_retrieve_hatch(self):
        return self.get_button_pressed_config(self.sysop_joystick, "hatch_autoretrieve")
        
    def auto_place_hatch(self):
        return self.get_button_pressed_config(self.sysop_joystick, "hatch_autoplace")

    def shift_drivetrain(self):
        return self.get_button_pressed_config(self.driver_joystick, "drivetrain_shift")

    def beast_mode(self):
        return self.get_button_pressed_config(self.driver_joystick, "beast_mode")

    def arcade_tank_shift(self):
        return self.get_button_pressed_config(self.driver_joystick, "arcade_tank_shift")

    def driver_override(self):
        return self.get_button_pressed_config(self.driver_joystick, "driver_override")