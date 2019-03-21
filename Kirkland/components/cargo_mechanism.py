from ctre import WPI_TalonSRX
from oi import OI
from utils import clamp

class CargoMechanism:
    cargo_mechanism_motor : WPI_TalonSRX
    oi : OI

    MINPOWER = -1
    MAXPOWER = 1

    def __init__(self):
        pass

    def execute(self):
        # TODO Thisll probably need to have varying power depending on direction
        # positive power makes the cargo tip inwards
        power = self.oi.process_cargo_control()
        power = clamp(power, CargoMechanism.MINPOWER, CargoMechanism.MAXPOWER)
        self.cargo_mechanism_motor.set(power)