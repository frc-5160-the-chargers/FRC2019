from wpilib import DoubleSolenoid

class HatchExtend:
    def __init__(self, hatch_extension_actuator_left, hatch_extension_actuator_right):
        self.extended = False
        self.hatch_extension_actuator_left = hatch_extension_actuator_left
        self.hatch_extension_actuator_right = hatch_extension_actuator_right

    def extend_hatch(self):
        self.extended = True
    
    def retract_hatch(self):
        self.extended = False

    def toggle_state(self):
        self.extended = not self.extended
    
    def execute(self):
        if self.extended:
            self.hatch_extension_actuator_left.set(DoubleSolenoid.Value.kForward)
            self.hatch_extension_actuator_right.set(DoubleSolenoid.Value.kForward)
        elif not self.extended:
            self.hatch_extension_actuator_left.set(DoubleSolenoid.Value.kReverse)
            self.hatch_extension_actuator_right.set(DoubleSolenoid.Value.kReverse)