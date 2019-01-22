from wpilib import DoubleSolenoid

class HatchGrab:
    hatch_grab_actuator : DoubleSolenoid

    def grab_hatch(self):
        self.hatch_grab_actuator.set(DoubleSolenoid.Value.kReverse)
    
    def release_hatch(self):
        self.hatch_grab_actuator.set(DoubleSolenoid.Value.kForward)