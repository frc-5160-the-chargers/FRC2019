from components.cargo_mechanism import CargoMechanism
from components.navx import NavX
from components.drivetrain import Drivetrain, DriveModes
from components.pneumatic_assemblies import HatchGrab, HatchRack, Shifters
from components.pressure_sensor import AnalogPressureSensor
from components.cargo_servo import CargoServo, CargoServoPosition

from oi import OI, Side

import wpilib

class MainAutonomous:
    MODE_NAME = "Main autonomous"
    DEFAULT = True

    # components
    cargo_mechanism :   CargoMechanism
    navx_board :        NavX
    drivetrain :        Drivetrain
    hatch_rack :        HatchRack
    hatch_grab :        HatchGrab
    gearbox_shifters :  Shifters
    cargo_lock :        CargoServo

    oi : OI

    def on_enable(self):
        """
        Called when the robot starts; optional
        """
        self.oi.load_user_settings()
        self.navx_board.reset_rotation()
        self.drivetrain.reset_input()
        self.drivetrain.current_mode = DriveModes.DRIVEROPERATED
        self.oi.arcade_drive = True

    def on_disable(self):
        pass
    
    def on_iteration(self, time_elapsed):
        """
        Called on each iteration of the control loop for both auton and tele
        """
        # TODO Since this is the same code as teleop, there should be some way to consolidate it into one function
        # TODO Individual try catches
        try:
            # set drivetrain power
            if self.drivetrain.current_mode == DriveModes.DRIVEROPERATED:
                if self.oi.arcade_drive:
                    self.drivetrain.teleop_drive_robot(speed=self.oi.process_driver_input(Side.LEFT), rotation=self.oi.process_driver_input(Side.RIGHT))
                else:
                    self.drivetrain.teleop_drive_robot(left_speed=self.oi.process_driver_input(Side.LEFT), right_speed=self.oi.process_driver_input(Side.RIGHT))

            # BEAST MODE
            if self.oi.beast_mode():
                self.oi.beast_mode_active = not self.oi.beast_mode_active

            # handle the cargo mechanism
            if self.oi.toggle_cargo_lock():
                self.cargo_lock.toggle_lock()

            # operate the hatch mechanism
            # the drawer
            if self.oi.extend_hatch():
                self.hatch_rack.toggle_state()
            # grabber
            if self.oi.grab_hatch():
                self.hatch_grab.toggle_state()

            # shift the drivetrain gear ratios
            if self.oi.shift_drivetrain():
                # shift the drivetrain
                self.gearbox_shifters.toggle_shift()

            # if self.oi.arcade_tank_shift():
            #     self.oi.arcade_drive = not self.oi.arcade_drive

            if self.cargo_lock.current_position == CargoServoPosition.UNLOCKED:
                self.cargo_mechanism.power = self.oi.process_cargo_control()
            else:
                self.cargo_mechanism.power = 0

            # booleans to indicate grabber status
            wpilib.SmartDashboard.putString("hatch grabber status", "Latched" if self.hatch_grab.latched else "Not Latched")
            wpilib.SmartDashboard.putString("hatch rack status", "Extended" if self.hatch_rack.extended else "Retracted")

            wpilib.SmartDashboard.putString("Tank drive", "Active" if self.drivetrain.current_mode != self.oi.arcade_drive else "Disabled")
            wpilib.SmartDashboard.putString("Beast mode", "Active" if self.oi.beast_mode_active else "Disabled")

        except:
            pass