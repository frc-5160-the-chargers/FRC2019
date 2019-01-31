from wpilib import DoubleSolenoid

class GearboxShifter:
    gearbox_shifter_actuator : DoubleSolenoid

    LOW = DoubleSolenoid.Value.kForward
    HIGH = DoubleSolenoid.Value.kReverse

    def __init__(self):
        self.position = GearboxShifter.LOW

    def shift_up(self):
        self.position = GearboxShifter.HIGH
    
    def shift_down(self):
        self.position = GearboxShifter.LOW

    def toggle_shift(self):
        self.position = GearboxShifter.LOW if self.position == GearboxShifter.HIGH else GearboxShifter.HIGH
    
    def execute(self):
        self.gearbox_shifter_actuator.set(self.position)