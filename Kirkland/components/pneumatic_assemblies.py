from wpilib import DoubleSolenoid

class Shifters:
    LOW = DoubleSolenoid.Value.kForward
    HIGH = DoubleSolenoid.Value.kReverse
    OFF = DoubleSolenoid.Value.kOff

    left_shifter_actuator : DoubleSolenoid
    right_shifter_actuator : DoubleSolenoid

    def __init__(self):
        self.position = Shifters.LOW

    def shift_up(self):
        self.position = Shifters.HIGH
    
    def shift_down(self):
        self.position = Shifters.LOW
    
    def toggle_shift(self):
        self.position = Shifters.LOW if self.position == Shifters.HIGH else Shifters.HIGH
    
    def execute(self):
        self.left_shifter_actuator.set(self.position)
        self.right_shifter_actuator.set(self.position)

class HatchGrab:
    hatch_grab_actuator : DoubleSolenoid

    def __init__(self):
        self.latched = False
    
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

class HatchRack:
    hatch_extension_actuator_left : DoubleSolenoid
    hatch_extension_actuator_right : DoubleSolenoid

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
            self.hatch_extension_actuator_left.set(DoubleSolenoid.Value.kForward)
            self.hatch_extension_actuator_right.set(DoubleSolenoid.Value.kForward)
        elif not self.extended:
            self.hatch_extension_actuator_left.set(DoubleSolenoid.Value.kReverse)
            self.hatch_extension_actuator_right.set(DoubleSolenoid.Value.kReverse)