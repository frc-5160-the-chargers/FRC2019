import time
import serial
# import arduino.serial_spoofed as serial # NOTE comment this to enable debug spoofing
import re
from threading import Thread
import math

class Vector:
    def __init__(self, inStr=None):
        if inStr != None:
            inStr = str(inStr).split(")")
            pair1 = inStr[0][9:].split(" ")
            pair2 = inStr[1][2:].split(" ")
            self.originPoint = [int(pair1[0]), int(pair1[1])]
            self.endPoint = [int(pair2[0]), int(pair2[1])]
        else:
            self.originPoint = [0, 0]
            self.endPoint = [0, 0]
        # 0 0 is the top left
        self.compound = [self.endPoint[0]-self.originPoint[0], self.endPoint[1]-self.originPoint[1]]
        self.slope = self.compound[1]/self.compound[0] if self.compound[0] != 0 else 0
        self.yIntercept = self.slope*(-self.originPoint[0])+self.originPoint[1]
        self.vectorDetected = self.originPoint[0] > 0 and self.originPoint[0] < 100 and self.endPoint[0] > -0 and self.endPoint[0] < 100
        self.realSlope = self.compound[0] != 0
        self.center = self.originPoint[0] + ((self.endPoint[0] - self.originPoint[0]) / 2)
        self.closestX = self.endPoint[0] if self.endPoint[1] > self.originPoint[1] else self.originPoint[0]

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
        angle = math.atan2(b, a)
        return math.degrees(angle)

    def getYFromX(self, x):
        return self.slope*x+self.yIntercept

class ArduinoServer:
    def __init__(self, comPort="/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_8533234343235160F190-if00"):
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