from ctre import WPI_TalonSRX
from OI import OI
from wpilib import DigitalInput

class CargoMechanism:
    cargo_mechanism_motor : WPI_TalonSRX
    oi : OI
    inner_cargo_limit_switch : DigitalInput
    outer_cargo_limit_switch : DigitalInput

    def __init__(self):
        pass

    def execute(self):
        # positive power makes the cargo tip inwards
        power = self.oi.process_cargo_control()
        if (self.inner_cargo_limit_switch.get() and power > 0.05): # inner switch is not pressed
            self.cargo_mechanism_motor.set(power)
        elif (self.outer_cargo_limit_switch.get() and power < 0.05): # outer switch pressed
            self.cargo_mechanism_motor.set(power)
        else:
            self.cargo_mechanism_motor.set(0)