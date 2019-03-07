import magicbot
import wpilib
import wpilib.drive

import navx

import ctre

import robotmap
import OI
from OI import Side

from arduino.data_server import ArduinoServer
from motorConfigurator import MotorConfigurator

from components.drivetrain import Drivetrain
from components.hatch_extend import HatchExtend
from components.hatch_grab import HatchGrab
from components.gearbox_shifter import GearboxShifter
from components.ultrasonic_sensor_array import UltrasonicSensorArray
from components.analog_ultrasonic_sensor import AnalogUltrasonicSensor
from components.navx_handler import NavXHandler
from components.cargo_mechanism import CargoMechanism
from components.hatch_manager import HatchManager

class MyRobot(magicbot.MagicRobot):
    # components
    drivetrain : Drivetrain
    hatch_subsystem : HatchManager
    gyro : NavXHandler
    cargo_mechanism : CargoMechanism

    def createObjects(self):
        """
        Create motors and stuff here
        """

        # drivetrain motors
        self.right_front_motor = ctre.WPI_TalonSRX(robotmap.right_back_drive)
        self.right_back_motor = ctre.WPI_TalonSRX(robotmap.right_bottom_drive)
        self.right_top_motor = ctre.WPI_TalonSRX(robotmap.right_top_drive)
        self.left_back_motor = ctre.WPI_TalonSRX(robotmap.left_bottom_drive)
        self.left_front_motor = ctre.WPI_TalonSRX(robotmap.left_front_drive)
        self.left_top_motor = ctre.WPI_TalonSRX(robotmap.left_top_drive)

        # cargo mechanism motors
        self.cargo_mechanism_motor = ctre.WPI_TalonSRX(robotmap.cargo_motor)

        # pneumatic components
        # drawer extenders
        self.hatch_extension_actuator_left = wpilib.DoubleSolenoid(robotmap.hatch_extension_pcm, robotmap.hatch_extension_left_front, robotmap.hatch_extension_left_back)
        self.hatch_extension_actuator_right = wpilib.DoubleSolenoid(robotmap.hatch_extension_pcm, robotmap.hatch_extension_right_front, robotmap.hatch_extension_right_back)    
        self.hatch_extension = HatchExtend(self.hatch_extension_actuator_left, self.hatch_extension_actuator_right)
        # grabber
        self.hatch_grab_actuator = wpilib.DoubleSolenoid(robotmap.grabber_pcm, robotmap.hatch_grab_front, robotmap.hatch_grab_back)
        self.hatch_grabber = HatchGrab(self.hatch_grab_actuator)
        # shifters
        self.left_shifter_actuator = wpilib.DoubleSolenoid(robotmap.shifter_pcm, robotmap.shifter_left_front, robotmap.shifter_left_back)
        self.right_shifter_actuator = wpilib.DoubleSolenoid(robotmap.shifter_pcm, robotmap.shifter_right_front, robotmap.shifter_right_back)
        
        # gearbox shifters
        self.left_shifter = GearboxShifter(self.left_shifter_actuator)
        self.right_shifter = GearboxShifter(self.right_shifter_actuator)

        # configure motors - current limit, ramp rate, etc.
        MotorConfigurator.bulk_config_drivetrain(self.right_front_motor, self.right_back_motor, self.right_top_motor, self.left_front_motor, self.left_back_motor, self.left_top_motor)

        # create motor groups based on side
        self.left_drive_motors = wpilib.SpeedControllerGroup(self.left_back_motor, self.left_front_motor, self.left_top_motor)
        self.right_drive_motors = wpilib.SpeedControllerGroup(self.right_front_motor, self.right_back_motor, self.right_top_motor)

        # create drivetrain based on groupings
        self.drive = wpilib.drive.DifferentialDrive(self.left_drive_motors, self.right_drive_motors)

        # limit switches
        self.inner_cargo_limit_switch = wpilib.DigitalInput(robotmap.cargo_limit_switch_inside)
        self.outer_cargo_limit_switch = wpilib.DigitalInput(robotmap.cargo_limit_switch_outside)

        # navx board
        self.navx = navx.AHRS.create_spi()

        # oi class
        self.oi = OI.OI()

        # code to run the pixy cam server
        # self.pixy_cam_server = ArduinoServer()
        # self.pixy_cam_server.startServer()          # launch a new thread for it

        # launch automatic camera capturing for main drive cam
        wpilib.CameraServer.launch()

        # PID tuning params
        self.driveLabels = ["dKP", "dKI", "dKD"]
        self.turnLabels = ["tKP", "tKI", "tKD"]

        for i in self.driveLabels:
            wpilib.SmartDashboard.putNumber(i, 0.1)
        for i in self.turnLabels:
            wpilib.SmartDashboard.putNumber(i, 0.1)

    def teleopInit(self):
        """
        Called when teleop starts; optional
        """
        #self.oi.write_settings()
        self.oi.load_user_settings()
        self.gyro.reset_rotation()
        self.drivetrain.reset_encoders()

        # self.drivetrain.pid.set_setpoint_reset(self.drivetrain.TICKS_PER_INCH*12)
        # self.drivetrain.turn_to_position(90, timeout=5)


    def teleopPeriodic(self):
        """
        Called on each iteration of the control loop
        """
        try:
            # operate the hatch mechanism
            # the drawer
            if self.oi.hatch_extend_control():
                self.hatch_extension.toggle_state()
            # grabber
            if self.oi.hatch_grab_control():
                self.hatch_grabber.toggle_state()

            # shift the drivetrain gear ratios
            if self.oi.drivetrain_shifting_control():
                self.drivetrain.shift()

            # this part does the mode switching for driver control
            # TODO: move into OI
            if wpilib.XboxController(0).getAButtonPressed():
                self.oi.beastMode = not self.oi.beastMode
            if wpilib.XboxController(0).getXButtonPressed():
                self.drivetrain.toggle_tankdrive()

            # yeah so we need a button to load in the PID constants
            if wpilib.XboxController(2).getAButtonPressed():
                self.drivetrain.drivePIDToleranceController.updateConstants(
                    kP=wpilib.SmartDashboard.getNumber(self.driveLabels[0], 0),
                    kI=wpilib.SmartDashboard.getNumber(self.driveLabels[1], 0),
                    kD=wpilib.SmartDashboard.getNumber(self.driveLabels[2], 0)
                )
                self.drivetrain.turnPIDToleranceController.updateConstants(
                    kP=wpilib.SmartDashboard.getNumber(self.turnLabels[0], 0),
                    kI=wpilib.SmartDashboard.getNumber(self.turnLabels[1], 0),
                    kD=wpilib.SmartDashboard.getNumber(self.turnLabels[2], 0)
                )
            if wpilib.XboxController(2).getBButtonPressed():
                self.drivetrain.driver_takeover()
            # and obviously with that comes a need for a way to switch between different test modes
            if wpilib.XboxController(2).getXButtonPressed():
                self.drivetrain.start_turn_to_position(90, timeout=200, tolerance=0.1, timeStable=100)
            if wpilib.XboxController(2).getYButtonPressed():
                self.drivetrain.start_drive_to_position(12*3, timeout=200, tolerance=0.1, timeStable=100)
        except:
            self.onException()


if __name__ == '__main__':
    wpilib.run(MyRobot)
