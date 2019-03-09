from components.drivetrain import Drivetrain, DriveModes
from components.hatch_manager import HatchManager
from OI import OI, Side
from components.analog_pressure_sensor import AnalogPressureSensor

import wpilib

class MainAutonomous:
    MODE_NAME = "Main autonomous"

    DEFAULT = True

    drivetrain : Drivetrain
    hatch_subsystem : HatchManager
    oi : OI
    pressure_sensor : AnalogPressureSensor

    def on_enable(self):
        self.oi.load_user_settings()
        self.oi.beastMode = False
        self.drivetrain.currentMode = DriveModes.ARCADEDRIVE
    
    def on_disable(self):
        pass
    
    def on_iteration(self, time_elapsed):
        try:
            if self.oi.twoStickMode:
                self.drivetrain.teleop_drive_robot(self.oi.twoStickMode, self.oi.process_driver_input(Side.LEFT), self.oi.process_driver_input(Side.RIGHT), square_inputs=True)
            else:
                self.drivetrain.teleop_drive_robot(self.oi.twoStickMode, self.oi.process_driver_input(Side.LEFT), self.oi.process_driver_input(Side.RIGHT), square_inputs=True)

            if self.oi.hatch_extend_control():
                self.hatch_subsystem.hatch_extension.toggle_state()
            # grabber
            if self.oi.hatch_grab_control():
                self.hatch_subsystem.hatch_grabber.toggle_state()

            # shift the drivetrain gear ratios
            if self.oi.drivetrain_shifting_control():
                self.drivetrain.shift()

            # this part does the mode switching for driver control
            # TODO: move into OI
            if wpilib.XboxController(0).getAButtonPressed():
                self.oi.beastMode = not self.oi.beastMode
            if wpilib.XboxController(0).getXButtonPressed():
                self.drivetrain.toggle_tankdrive()

            wpilib.SmartDashboard.putNumber("Uncalibrated Pressure", self.pressure_sensor.get_uncalibrated_pressure_psi())

            # booleans to indicate grabber status
            wpilib.SmartDashboard.putString("hatch grabber status", "Latched" if self.hatch_subsystem.hatch_grabber.latched else "Not Latched")
            wpilib.SmartDashboard.putString("hatch rack status", "Extended" if self.hatch_subsystem.hatch_extension.extended else "Retracted")

            wpilib.SmartDashboard.putString("Tank drive", "Enabled" if self.drivetrain.currentMode == DriveModes.TANKDRIVE else "Disabled")
            wpilib.SmartDashboard.putString("Beast mode", "Enabled" if self.oi.beastMode else "Disabled")
        except:
            print("Tell John something isnt working quite right")