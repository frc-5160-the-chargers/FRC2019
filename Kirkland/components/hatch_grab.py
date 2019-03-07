from wpilib import DoubleSolenoid

class HatchGrab:
    def __init__(self, hatch_grab_actuator):
        self.latched = False
        self.hatch_grab_actuator = hatch_grab_actuator

    def grab_hatch(self):
        self.latched = True
    
    def release_hatch(self):
        self.latched = False
    
    def toggle_state(self):
        self.latched = not self.latched

    def execute(self):
        if self.latched:
            self.hatch_grab_actuator.set(DoubleSolenoid.Value.kReverse)
        elif not self.latched:
            self.hatch_grab_actuator.set(DoubleSolenoid.Value.kForward)
