from wpilib import DoubleSolenoid

class HatchExtend:
    hatch_extension_actuator : DoubleSolenoid

    def __init__(self):
        self.extended = False

    def extend_hatch(self):
        self.extended = True
    
    def retract_hatch(self):
        self.extended = False

    def toggle_state(self):
        self.extended = not self.extended
    
    def execute(self):
        if self.extended:
            self.hatch_extension_actuator.set(DoubleSolenoid.Value.kForward)
        elif not self.extended:
            self.hatch_extension_actuator.set(DoubleSolenoid.Value.kReverse)