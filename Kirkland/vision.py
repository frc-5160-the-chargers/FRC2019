#This comes from here: https://github.com/robotpy/robotpy-cscore/blob/master/examples/switched_cameraserver.py
#Also reference this CD thread: https://www.chiefdelphi.com/t/two-cameras-and-switching/348756/3

from cscore import CameraServer, UsbCamera
import networktables


def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()

    usb0 = UsbCamera("Camera 0", 0)
    usb1 = UsbCamera("Camera 1", 1)

    server = cs.addSwitchedCamera("Switched")
    server.setSource(usb0)

    # Use networktables to switch the source
    # -> obviously, you can switch them however you'd like
    def _listener(source, key, value, isNew):
        if str(value) == "0":
            server.setSource(usb0)
        elif str(value) == "1":
            server.setSource(usb1)

    table = networktables.NetworkTables.getTable("/CameraPublisher")
    table.putString("selected", "0")
    table.addEntryListener(_listener, key="selected")

    cs.waitForever()


if __name__ == "__main__":

    # To see messages from networktables, you must setup logging
    import logging

    logging.basicConfig(level=logging.DEBUG)

    # You should change this to connect to the RoboRIO
    networktables.NetworkTables.initialize(server="roborio-5160-frc.local")

    main()