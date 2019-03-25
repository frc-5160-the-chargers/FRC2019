PARITY_ODD = 0
STOPBITS_TWO = 0
SEVENBITS = 0

class Serial:
    def __init__(self, port=None, baudrate=None, parity=None, stopbits=None, bytesize=None):
        self.vector1 = [38, 51]
        self.vector2 = [39, 9]

    def readline(self):
        return "vector: ({} {}) ({} {}) index: 0 flags 4".format(self.vector1[0], self.vector1[1], self.vector2[0], self.vector2[1])