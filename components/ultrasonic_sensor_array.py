from components.analog_ultrasonic_sensor import AnalogUltrasonicSensor

class UltrasonicSensorArray:
    def __init__(self, ultrasonic_sensor_left, ultrasonic_sensor_right):
        self.last_left_measurement = -1
        self.last_right_measurement = -1
        self.ultrasonic_sensor_left = ultrasonic_sensor_left
        self.ultrasonic_sensor_right = ultrasonic_sensor_right
    
    def get_last_measurement_cm(self):
        return (self.last_left_measurement+self.last_right_measurement)/2

    def execute(self):
        left = self.ultrasonic_sensor_left.getDistanceCm()
        right = self.ultrasonic_sensor_right.getDistanceCm()

        self.last_right_measurement = right if right >= 30 else self.last_right_measurement
        self.last_left_measurement = left if left >= 30 else self.last_left_measurement