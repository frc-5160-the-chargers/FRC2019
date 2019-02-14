import time
import serial
import re


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

    def getYFromX(self, x):
        return self.slope*x+self.yIntercept


serialConnnection = serial.Serial(
    port="COM20",
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

serialConnnection.isOpen()

pattern = re.compile(r"vector: (\([0-9]+ [0-9]+\) ){2}index: [0-9]+ flags [0-9]+\r\n")

while True:
    line = str(serialConnnection.readline().decode())
    if pattern.match(line) != None:
        print(str(Vector(line)))

serialConnnection.close()