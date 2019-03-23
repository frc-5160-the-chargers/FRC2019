import magicbot
import wpilib
import ctre
import navx

from components.pressure_sensor import AnalogPressureSensor
from components.navx import NavX
from components.drivetrain import Drivetrain
from components.pneumatic_assemblies import HatchGrab, HatchRack, Shifters
from components.cargo_mechanism import CargoMechanism

from controllers.drivetrain_pid import DriveStraightPID, TurnPID

import robotmap
from motor_configurator import configure_cargo_redline, bulk_config_drivetrain 
from oi import OI, Side

class MyRobot(magicbot.MagicRobot):
    # components
    cargo_mechanism :   CargoMechanism
    navx_board :        NavX
    drivetrain :        Drivetrain
    hatch_rack :        HatchRack
    hatch_grab :        HatchGrab
    gearbox_shifters :  Shifters

    controller_drive_straight : DriveStraightPID
    controller_turn :           TurnPID

    def createObjects(self):
        """
        Create motors and stuff here
        """
        # DRIVETRAIN
        # drivetrain motors
        self.right_front_motor = ctre.WPI_TalonSRX(robotmap.right_back_drive)
        self.right_back_motor = ctre.WPI_TalonSRX(robotmap.right_bottom_drive)
        self.right_top_motor = ctre.WPI_TalonSRX(robotmap.right_top_drive)
        self.left_back_motor = ctre.WPI_TalonSRX(robotmap.left_bottom_drive)
        self.left_front_motor = ctre.WPI_TalonSRX(robotmap.left_front_drive)
        self.left_top_motor = ctre.WPI_TalonSRX(robotmap.left_top_drive)

        # configure motors - current limit, ramp rate, etc.
        bulk_config_drivetrain(self.right_front_motor, self.right_back_motor, self.right_top_motor, self.left_front_motor, self.left_back_motor, self.left_top_motor)

        # create motor groups based on side
        self.left_drive_motors = wpilib.SpeedControllerGroup(self.left_back_motor, self.left_front_motor, self.left_top_motor)
        self.right_drive_motors = wpilib.SpeedControllerGroup(self.right_front_motor, self.right_back_motor, self.right_top_motor)

        # create drivetrain based on groupings
        self.drive = wpilib.drive.DifferentialDrive(self.left_drive_motors, self.right_drive_motors)


        # CARGO MECHANISM
        # cargo mechanism motors
        self.cargo_mechanism_motor = ctre.WPI_TalonSRX(robotmap.cargo_motor)
        configure_cargo_redline(self.cargo_mechanism_motor)


        # PNEUMATICS
        # drawer extenders
        self.hatch_extension_actuator_left = wpilib.DoubleSolenoid(robotmap.hatch_extension_pcm, robotmap.hatch_extension_left_front, robotmap.hatch_extension_left_back)
        self.hatch_extension_actuator_right = wpilib.DoubleSolenoid(robotmap.hatch_extension_pcm, robotmap.hatch_extension_right_front, robotmap.hatch_extension_right_back)    

        # grabber
        self.hatch_grab_actuator = wpilib.DoubleSolenoid(robotmap.grabber_pcm, robotmap.hatch_grab_front, robotmap.hatch_grab_back)

        # shifters
        self.left_shifter_actuator = wpilib.DoubleSolenoid(robotmap.shifter_pcm, robotmap.shifter_left_front, robotmap.shifter_left_back)
        self.right_shifter_actuator = wpilib.DoubleSolenoid(robotmap.shifter_pcm, robotmap.shifter_right_front, robotmap.shifter_right_back)

        # pressure sensor
        self.pressure_sensor = AnalogPressureSensor(1)
        
        # MISC/SENSORS
        # navx board
        self.navx = navx.AHRS.create_spi()

        # oi class
        self.oi = OI()

        # pid controllers
        self.drive_forwards_pid = wpilib.PIDController(
                                    robotmap.drive_kP,
                                    robotmap.drive_kI, 
                                    robotmap.drive_kD,
                                    lambda: self.drivetrain.get_average_position(),
                                    lambda x: self.drivetrain.teleop_drive_robot(speed=x))
        self.turn_pid = wpilib.PIDController(
                                    robotmap.turn_kP,
                                    robotmap.turn_kI,
                                    robotmap.turn_kD,
                                    lambda: self.navx_board.get_rotation(),
                                    lambda x: self.drivetrain.teleop_drive_robot(rotation=x))
        self.drive_forwards_pid.setToleranceBuffer(robotmap.drive_buffer)
        self.turn_pid.setToleranceBuffer(robotmap.turn_buffer)

        # launch automatic camera capturing for main drive cam
        wpilib.CameraServer.launch("vision.py:main")

    def teleopInit(self):
        """
        Called when the robot starts; optional
        """
        self.oi.load_user_settings()
        self.navx_board.reset_rotation()
        
    def teleopPeriodic(self):
        """
        Called on each iteration of the control loop for both auton and tele
        """
        # TODO Individual try catches
        try:
            # set drivetrain power
            if self.oi.arcade_drive:
                self.drivetrain.teleop_drive_robot(speed=self.oi.process_driver_input(Side.LEFT), rotation=self.oi.process_driver_input(Side.RIGHT))
            else:
                self.drivetrain.teleop_drive_robot(left_speed=self.oi.process_driver_input(Side.LEFT), right_speed=self.oi.process_driver_input(Side.RIGHT))

            #calibrate the analog pressure sensor
            if self.oi.calibrate_pressure_sensor():
                self.pressure_sensor.calibrate_pressure()

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

            # this part does the mode switching for driver control
            if self.oi.beast_mode():
                self.oi.beast_mode_active = not self.oi.beast_mode_active

            if self.oi.arcade_tank_shift():
                self.oi.arcade_drive = not self.oi.arcade_drive
            
            # driver override for PID loops
            if self.oi.driver_override():
                self.drivetrain.driver_takeover()

            #display calibrated air pressure in smart dashboard
            wpilib.SmartDashboard.putNumber("Calibrated Pressure", self.pressure_sensor.get_pressure_psi())
            
            # calibrate if needed
            if self.oi.calibrate_pressure_sensor():
                self.pressure_sensor.calibrate_pressure()

            # booleans to indicate grabber status
            wpilib.SmartDashboard.putString("hatch grabber status", "Latched" if self.hatch_grab.latched else "Not Latched")
            wpilib.SmartDashboard.putString("hatch rack status", "Extended" if self.hatch_rack.extended else "Retracted")

            wpilib.SmartDashboard.putString("Tank drive", "Active" if self.drivetrain.current_mode != self.oi.arcade_drive else "Disabled")
            wpilib.SmartDashboard.putString("Beast mode", "Active" if self.oi.beast_mode_active else "Disabled")
        except:
            self.onException()


if __name__ == '__main__':
    wpilib.run(MyRobot)
