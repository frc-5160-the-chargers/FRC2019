from magicbot import StateMachine, state, timed_state

from components.drivetrain import DriveModes, Drivetrain
from components.pneumatic_assemblies import Shifters
from components.arduino import ArduinoHandler

from wpilib import PIDController

import utils
import robotmap

class AlignmentController(StateMachine):
    drivetrain :        Drivetrain
    gearbox_shifters :  Shifters

    arduino_component : ArduinoHandler

    def stop_reset_drivetrain(self):
        self.drivetrain.stop_motors()
        self.drivetrain.driver_takeover()

    def line_detect_failsafe_checker(self):
        if not self.arduino_component.safe_to_detect():
            self.interrupt()

    def interrupt(self):
        self.stop_reset_drivetrain()
        self.done()

    def drive_with_alignment(self, position):
        alignmentMaxSpeed = .75
        straightTolerance = 3 # withing pixyunits for alignment tolerance
        p = utils.clamp(utils.root(-position*robotmap.drive_power_constant, 5), -alignmentMaxSpeed, alignmentMaxSpeed) # we take the 3rd root here to curve the power a bit, its like ghetto pid
        if -position > straightTolerance:
            self.drivetrain.teleop_drive_robot(left_speed=p*robotmap.drive_power_side_ratio, right_speed=-p)
        elif -position < -straightTolerance:
            self.drivetrain.teleop_drive_robot(left_speed=p, right_speed=-p*robotmap.drive_power_side_ratio)
        else:
            self.drivetrain.teleop_drive_robot(left_speed=-0.5, right_speed=-0.5)
        self.line_detect_failsafe_checker()

    def start_alignment(self):
        # see if we should even start based on line detection failures
        if self.arduino_component.safe_to_detect():
            self.drivetrain.current_mode = DriveModes.ALIGNMENTOPERATED
            self.engage()

    @state(first=True)
    def shift_gearboxes(self):
        self.gearbox_shifters.shift_down()
        self.next_state_now('alignment_process')

    @timed_state(duration=50, must_finish=True, next_state='stop_alignment_process')
    def alignment_process(self):
        # NOTE so for this, just look at the average line position and apply power as needed based on it
        # see the line-alignment-routine.md document for more info
        # average bottom line position is used so the robot will try to align with the bottom of the line first
        self.drive_with_alignment(self.arduino_component.average_line_position)
        # wait there's no way its literally 3 lines of code wtf
        # ok failsafe adds more...
        self.line_detect_failsafe_checker()
    
    @state(must_finish=True)
    def stop_alignment_process(self):
        self.stop_reset_drivetrain()
        self.done()