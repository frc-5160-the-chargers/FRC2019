from cscore import CameraServer

def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()

    usb1 = cs.startAutomaticCapture(dev=0)

    cs.waitForever()