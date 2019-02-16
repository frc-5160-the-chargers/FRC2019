from navx import AHRS

class NavXHandler:
    navx : AHRS

    def __init__(self):
        self.last_rotation = 0# self.get_rotation()

    def get_rotation(self):
        return self.navx.getRawGyroZ()

    def reset_rotation(self):
        self.navx.reset() 

    def execute(self):
        self.last_rotation = self.get_rotation()