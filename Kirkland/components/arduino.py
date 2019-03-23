from arduino.data_server import ArduinoServer, Vector

import robotmap

class ArduinoHandler:
    arduino_server :    ArduinoServer

    def __init__(self):
        self.last_lines = []
        self.average_line_position = 0  # note that this is the average x position or the "center" of the line detected
        self.failed_lines = 0            # number of times attempted since last detected line

    def safe_to_detect(self):
        return self.failed_lines < robotmap.gathering_time

    def execute(self):
        v = self.arduino_server.getVector()
        
       # NOTE hi future me, this code is basically just getting the average of the center of the lines. have fun deciphering it

        if v != None:
            self.failed_lines = 0
            if len(self.last_lines) > robotmap.gathering_buffer:
                self.last_lines.pop(0)
            self.last_lines.append(v)
            sumPositions = 0
            for i in self.last_lines:
                sumPositions += i.center-robotmap.camera_center
            self.average_line_position = sumPositions / len(self.last_lines)
        else:
            self.failed_lines += 1
