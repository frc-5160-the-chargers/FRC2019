import magicbot
import wpilib
import wpilib.drive

import robotmap
import OI
from OI import Side

import ctre

from components.drivetrain import Drivetrain
from components.hatch_extend import HatchExtend
from components.hatch_grab import HatchGrab
from components.gearbox_shifter import GearboxShifter

from motorConfigurator import MotorConfigurator

# flags
FBXC = True

class MyRobot(magicbot.MagicRobot):

    #High level components - list these first

    #Low level components
    drivetrain : Drivetrain
    hatch_grabber : HatchGrab
    hatch_extension : HatchExtend

    def createObjects(self):
        '''Create motors and stuff here'''

        #declare motors
        self.right_front_motor = ctre.WPI_TalonSRX(robotmap.front_right_drive)
        self.right_back_motor = ctre.WPI_TalonSRX(robotmap.back_right_drive)
        self.left_back_motor = ctre.WPI_TalonSRX(robotmap.back_left_drive)
        self.left_front_motor = ctre.WPI_TalonSRX(robotmap.front_left_drive)

        #declare pneumatic components
        self.hatch_extension_actuator = wpilib.DoubleSolenoid(robotmap.hatch_extension_one, robotmap.hatch_extension_two)
        self.hatch_grab_actuator = wpilib.DoubleSolenoid(robotmap.hatch_grab_one, robotmap.hatch_grab_two)
        self.left_shifter_actuator = wpilib.DoubleSolenoid(robotmap.shifter_left_one, robotmap.shifter_left_two)
        self.right_shifter_actuator = wpilib.DoubleSolenoid(robotmap.shifter_right_one, robotmap.shifter_right_two)

        # shifters
        self.left_shifter = GearboxShifter(self.left_shifter_actuator)
        self.right_shifter = GearboxShifter(self.right_shifter_actuator)

        #configure motors - current limit, ramp rate, etc.
        MotorConfigurator.bulk_config_drivetrain(self.right_front_motor, self.right_back_motor, self.left_front_motor, self.left_back_motor)

        #group motors
        self.left_drive_motors = wpilib.SpeedControllerGroup(self.left_back_motor, self.left_front_motor)
        self.right_drive_motors = wpilib.SpeedControllerGroup(self.right_front_motor, self.right_back_motor)
        
        #FBXC motors are oriented differently than on the newest chassis
        if FBXC:
            self.right_drive_motors.setInverted(True)
        else:
            self.left_drive_motors.setInverted(True)
        
        self.drive = wpilib.drive.DifferentialDrive(self.left_drive_motors, self.right_drive_motors)

        self.oi = OI.OI()

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        #self.oi.write_settings()
        self.oi.load_user_settings()


    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        try:
            #this part does the wheels
            if self.oi.twoStickMode:
                self.drivetrain.teleop_drive_robot(self.oi.twoStickMode, self.oi.process_driver_input(Side.LEFT), self.oi.process_driver_input(Side.RIGHT), square_inputs=True)
            else:
                self.drivetrain.teleop_drive_robot(self.oi.twoStickMode, self.oi.process_driver_input(Side.LEFT), self.oi.process_driver_input(Side.RIGHT), square_inputs=True)

            #operate the hatch mechanism
            if self.oi.hatch_extend_control():
                self.hatch_extension.toggle_state()
            
            if self.oi.hatch_grab_control():
                self.hatch_grabber.toggle_state()

            #shift the drivetrain gear ratios
            if self.oi.drivetrain_shifting_control():
                self.drivetrain.shift()

            #this part does the mode switching for driver control
            #TODO: Figure out how to make all references to the controller go into the OI
            if wpilib.XboxController(0).getAButtonPressed():
                self.oi.beastMode = not self.oi.beastMode
            if wpilib.XboxController(0).getXButtonPressed():
                self.oi.twoStickMode = not self.oi.twoStickMode
                
        except:
            self.onException()


if __name__ == '__main__':
    wpilib.run(MyRobot)