from magicbot import StateMachine, state, timed_state

from components.drivetrain import DriveModes, Drivetrain
from components.pneumatic_assemblies import Shifters
from components.arduino import ArduinoHandler

from wpilib import PIDController

import robotmap

class AlignmentController(StateMachine):
    drivetrain :        Drivetrain
    gearbox_shifters :  Shifters

    arduino_component : ArduinoHandler

    def start_alignment(self):
        # see if we should even start based on line detection failures
        if self.arduino_component.safe_to_detect():
            self.engage()

    @state(first=True)
    def shift_gearboxes(self):
        self.drivetrain.current_mode = DriveModes.ALIGNMENTOPERATED
        self.gearbox_shifters.shift_down()
        self.next_state_now('alignment_process')

    @timed_state(duration=3, must_finish=True)
    def alignment_process(self):
        # NOTE so for this, just look at the average line position and apply power as needed based on it
        # see the line-alignment-routine.md document for more info
        linePosition = self.arduino_component.average_line_position
        p = linePosition*robotmap.drive_power_constant
        self.drivetrain.teleop_drive_robot(left_power=p, right_power=-p)
        # wait there's no way its literally 3 lines of code wtf
        # ok failsafe adds more...
        if not self.arduino_component.safe_to_detect():
            self.drivetrain.stop_motors()
            self.drivetrain.driver_takeover()
            self.done()