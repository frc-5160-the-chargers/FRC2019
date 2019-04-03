from arduino.data_server import Vector

PARITY_ODD = 0
STOPBITS_TWO = 0
SEVENBITS = 0

class Serial:
    def __init__(self, port=None, baudrate=None, parity=None, stopbits=None, bytesize=None):
        self.vector1 = [38, 51]
        self.vector2 = [39, 9]

    def readline(self):
        return "vector: ({} {}) ({} {}) index: 0 flags 4".format(self.vector1[0], self.vector1[1], self.vector2[0], self.vector2[1])

class ArduinoServer:
    def __init__(self, comPort="/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_8533234343235160F190-if00"):
        self.lastVector = None
        self.vectorDetected = False
        self.vector1 = [int(78/2), 51]
        self.vector2 = [int(78/2)+5, 9]

    def collectData(self):
    # try:
        line = str("vector: ({} {}) ({} {}) index: 0 flags 4".format(self.vector1[0], self.vector1[1], self.vector2[0], self.vector2[1]))
        vector = Vector(line)
        self.vectorDetected = vector.vectorDetected
        self.lastVector = vector
        # except:
        #     pass
    
    def startServer(self):
        self.runServer()

    def runServer(self):
        self.collectData()

    def getVector(self):
        return None if not self.vectorDetected else self.lastVector