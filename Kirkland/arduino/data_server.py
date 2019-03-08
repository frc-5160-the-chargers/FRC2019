import time
import serial
import re
from threading import Thread
import math

class Vector:
    def __init__(self, inStr):
        inStr = str(inStr).split(")")
        pair1 = inStr[0][9:].split(" ")
        pair2 = inStr[1][2:].split(" ")
        self.originPoint = [int(pair1[0]), int(pair1[1])]
        self.endPoint = [int(pair2[0]), int(pair2[1])]
        self.compound = [self.endPoint[0]-self.originPoint[0], self.endPoint[1]-self.originPoint[1]]
        self.slope = self.compound[1]/self.compound[0] if self.compound[0] != 0 else 0
        self.yIntercept = self.slope*(-self.originPoint[0])+self.originPoint[1]
        self.vectorDetected = not (self.originPoint == [129, 0] and self.endPoint == [254, 188])
        self.realSlope = self.compound[0] != 0

    def __str__(self):
        if self.realSlope and self.vectorDetected:
            return "({}), y-int: {}".format(", ".join(list(map(str, self.compound))), str(self.yIntercept))
        elif self.vectorDetected:
            return "({}), infinite slope".format(", ".join(list(map(str, self.compound))))
        else:
            return "No vector detected"

    def getAngle(self):
        # first get the quadrant
        a = self.compound[0]
        b = -self.compound[1]
        angle = 0
        if a > 0 and b > 0:
            angle = math.atan(b/a)
        if a < 0 and b > 0:
            angle = 180+math.atan(b/a)
        if a < 0 and b < 0:
            angle = 180+math.atan(b/a)
        if a > 0 and b < 0:
            angle = 360+math.atan(b/a)
        return angle

    def getYFromX(self, x):
        return self.slope*x+self.yIntercept

class ArduinoServer:
    def __init__(self, comPort="/dev/ttyACM0"):
        self.serialConnnection = serial.Serial(
            port=comPort,
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )

        self.pattern = re.compile(r"vector: (\([0-9]+ [0-9]+\) ){2}index: [0-9]+ flags [0-9]+\r\n")

        self.lastVector = None
        self.vectorDetected = False

    def collectData(self):
        try:
            line = str(self.serialConnnection.readline().decode())
            if self.pattern.match(line) != None:
                vector = Vector(line)
                self.vectorDetected = vector.vectorDetected
                self.lastVector = vector
        except:
            pass
    
    def startServer(self):
        thread = Thread(target = self.runServer)
        thread.start()

    def runServer(self):
        while True:
            self.collectData()

    def getVector(self):
        return None if not self.vectorDetected else self.lastVector