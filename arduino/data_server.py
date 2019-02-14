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

    def __str__(self):
        return "({}), ({}), y-int: {}".format(", ".join(list(map(str, self.originPoint))), ", ".join(list(map(str, self.endPoint))), str(self.yIntercept))

    def solveForX(self):
        pass


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