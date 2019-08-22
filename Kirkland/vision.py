# NOTE: look here for switchign cameras https://github.com/robotpy/robotpy-cscore/blob/master/examples/switched_cameraserver.py

from cscore import CameraServer, UsbCamera
import networktables


class CameraConfig:
    cargo_name = "cargo"
    cargo_dev_address = "/dev/v4l/by-path/platform-ci_hdrc.0-usb-0:1.2.2:1.0-video-index0"

    hatch_name = "hatch"
    hatch_dev_address = "/dev/v4l/by-path/platform-ci_hdrc.0-usb-0:1.2.3:1.0-video-index0"

    front_name = "front"
    front_dev_address = "/dev/v4l/by-path/platform-ci_hdrc.0-usb-0:1.2.4:1.0-video-index0"


def main():
    camera_server = CameraServer.getInstance()
    camera_server.enableLogging()
    # TODO Use device addresses and sides here please
    
    cargo_camera = UsbCamera(name=CameraConfig.cargo_name, path=CameraConfig.cargo_dev_address)
    hatch_camera = UsbCamera(name=CameraConfig.hatch_name, path=CameraConfig.hatch_dev_address)
    front_camera = camera_server.startAutomaticCapture(name=CameraConfig.front_name, path=CameraConfig.front_dev_address)
    
    
    switching_server = camera_server.addSwitchedCamera("Switched")
    switching_server.setSource(hatch_camera)

    # Use networktables to switch the source
    # -> obviously, you can switch them however you'd like
    def _listener(source, key, value, isNew):
        if str(value) == "0":
            switching_server.setSource(hatch_camera)
        elif str(value) == "1":
            switching_server.setSource(cargo_camera)

    network_table = networktables.NetworkTables.getTable("/CameraPublisher")
    network_table.putString("Selected Camera", "0")
    network_table.addEntryListener(_listener, key="Selected Camera")

    camera_server.waitForever()