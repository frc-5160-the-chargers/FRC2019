# NOTE: look here for switchign cameras https://github.com/robotpy/robotpy-cscore/blob/master/examples/switched_cameraserver.py

from cscore import CameraServer, UsbCamera
import networktables


def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()
    # TODO Use device addresses and sides here please
    
    cargo = UsbCamera(name="cargo", path='/dev/v4l/by-path/platform-ci_hdrc.0-usb-0:1.2.2:1.0-video-index0')
    hatch = UsbCamera(name="hatch", path='/dev/v4l/by-path/platform-ci_hdrc.0-usb-0:1.2.3:1.0-video-index0')
    front = cs.startAutomaticCapture(name="front", path='/dev/v4l/by-path/platform-ci_hdrc.0-usb-0:1.2.4:1.0-video-index0')
    
    
    server = cs.addSwitchedCamera("Switched")
    server.setSource(hatch)

    # Use networktables to switch the source
    # -> obviously, you can switch them however you'd like
    def _listener(source, key, value, isNew):
        if str(value) == "0":
            server.setSource(hatch)
        elif str(value) == "1":
            server.setSource(cargo)

    table = networktables.NetworkTables.getTable("/CameraPublisher")
    table.putString("selected", "0")
    table.addEntryListener(_listener, key="selected")

    cs.waitForever()