import math

class OI:
    def __init__(self):
        self.beastMode = False
        self.twoStickMode = False

    def curve(self, i):
        return math.pow(i, 3)/1.25

    def deadzone(self, i):
        DZ = 0.1
        if i < -DZ:
            return i
        elif i > DZ:
            return i
        else:
            return 0

    def process(self, i):
        return self.deadzone(self.curve(i) * (-1 if self.beastMode else 1))