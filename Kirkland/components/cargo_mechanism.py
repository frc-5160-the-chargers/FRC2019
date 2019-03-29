from ctre import WPI_TalonSRX
from oi import OI
from utils import clamp

class CargoMechanism:
    cargo_mechanism_motor : WPI_TalonSRX
    oi : OI

    MINPOWER = -0.18
    MAXPOWER = .18

    def __init__(self):
        self.power = 0

    def execute(self):
        # TODO Thisll probably need to have varying power depending on direction
        # positive power makes the cargo tip inwards
        power = clamp(-self.power, CargoMechanism.MINPOWER, CargoMechanism.MAXPOWER)
        self.cargo_mechanism_motor.set(power)