from navx import AHRS

class NavX:
    navx : AHRS

    def __init__(self):
        self.last_rotation = 0

    def get_rotation(self):
        return self.navx.getAngle()

    def reset_rotation(self):
        self.navx.reset()

    def execute(self):
        self.last_rotation = self.get_rotation()