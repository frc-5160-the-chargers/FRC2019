from wpilib import DoubleSolenoid

class GearboxShifter:
    LOW = DoubleSolenoid.Value.kForward
    HIGH = DoubleSolenoid.Value.kReverse

    def __init__(self, actuator):
        self.gearbox_shifter_actuator = actuator
        self.position = GearboxShifter.LOW

    def ready_to_shift(self):
        """Check motor velocities from encoders to determine if ready to shift. Return boolean. """
        pass

    def shift_up(self):
        self.position = GearboxShifter.HIGH
    
    def shift_down(self):
        self.position = GearboxShifter.LOW

    def toggle_shift(self):
        self.position = GearboxShifter.LOW if self.position == GearboxShifter.HIGH else GearboxShifter.HIGH
    
    def execute(self):
        self.gearbox_shifter_actuator.set(self.position)