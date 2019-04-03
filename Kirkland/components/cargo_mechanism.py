from ctre import WPI_TalonSRX
from oi import OI
from utils import clamp

class CargoMechanism:
    cargo_mechanism_motor : WPI_TalonSRX
    oi : OI

    POWERIN = -0.25
    POWEROUT = 0.2

    def __init__(self):
        self.power = 0

    def execute(self):
        # TODO Thisll probably need to have varying power depending on direction
        power = clamp(-self.power, CargoMechanism.POWERIN, CargoMechanism.POWEROUT)
        power = clamp(-self.power, CargoMechanism.POWERIN, CargoMechanism.POWEROUT)
        self.cargo_mechanism_motor.set(power)