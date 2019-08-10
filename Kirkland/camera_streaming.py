# camera_streaming.py
# code to run all the vision, but specifically just camera streaming

# camera switching borrowed from:
# https://github.com/robotpy/robotpy-cscore/blob/master/examples/switched_cameraserver.py

from cscore import CameraServer, UsbCamera
import networktables
from Kirkland import robotmap


def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()

    # no switching on front, just auto capture
    front_camera = cs.startAutomaticCapture(
        name=robotmap.Cameras.front_name, path=robotmap.Cameras.front_dev_address)

    # these two cameras are switched between, so no need to do auto capturing
    cargo_camera = UsbCamera(
        name=robotmap.Cameras.cargo_name, path=robotmap.Cameras.cargo_dev_address)
    hatch_camera = UsbCamera(
        name=robotmap.Cameras.hatch_name, path=robotmap.Cameras.hatch_dev_address)

    # camera switching networktables stuff
    switching_server = cs.addSwitchedCamera("Switched")
    switching_server.setSource(hatch_camera)  # default to hatch camera

    # listener to determine how to switch the cameras
    def _listener(source, key, value, isNew):
        if str(value) == "0":
            switching_server.setSource(hatch_camera)
        elif str(value) == "1":
            switching_server.setSource(cargo_camera)

    # publish to networktables
    camera_table = networktables.NetworkTables.getTable("/CameraPublisher")
    camera_table.putString("Selected Camera", "0")
    camera_table.addEntryListener(_listener, key="Selected Camera")

    cs.waitForever()
