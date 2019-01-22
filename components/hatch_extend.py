from wpilib import DoubleSolenoid

class HatchExtend:
    hatch_extension_actuator : DoubleSolenoid

    def extend_hatch(self):
        self.hatch_extension_actuator.set(DoubleSolenoid.Value.kForward)
    
    def retract_hatch(self):
        self.hatch_extension_actuator.set(DoubleSolenoid.Value.kReverse)