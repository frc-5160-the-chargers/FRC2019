import math

class OI:
    DEADZONE = 0.1

    def __init__(self):
        self.beastMode = False
        self.twoStickMode = False

    def curve(self, i):
        return math.pow(i, 3)/1.25

    def deadzone(self, i):
        if i < -OI.DEADZONE:
            return i
        elif i > OI.DEADZONE:
            return i
        else:
            return 0

    def process(self, i):
        return self.deadzone(self.curve(i) * (-1 if self.beastMode else 1))