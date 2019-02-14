import time
import serial

serialConnnection = serial.Serial(
    port="COM19",
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

serialConnnection.isOpen()

print(serialConnnection.readline())
serialConnnection.close()