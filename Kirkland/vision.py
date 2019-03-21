# NOTE: look here for switchign cameras https://github.com/robotpy/robotpy-cscore/blob/master/examples/switched_cameraserver.py

from cscore import CameraServer, UsbCamera
import networktables


def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()
    # TODO Use device addresses and sides here please
    usb0 = cs.startAutomaticCapture(dev=0)
    usb1 = cs.startAutomaticCapture(dev=1)
    cs.waitForever()