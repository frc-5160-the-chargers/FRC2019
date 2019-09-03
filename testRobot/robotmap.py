import math

# drivetrain
left_front_drive = 1
left_back_drive = 2
right_front_drive = 3
right_back_drive = 4

# encoders
left_encoder_a = 0
left_encoder_b = 1
right_encoder_a = 2
right_encoder_b = 3

# wheel diameter
wheel_diameter = 6

inches_per_tick = (6*math.pi)/256

# PID constants
# driving
drive_kP = 0.2
drive_kI = 0
drive_kD = 0

# turning
turn_kP = 0.1
turn_kI = 0
turn_kD = 0


# Constants for the arduino server logic
gathering_buffer = 1       # take the last x vectors to calculate
gathering_time = 15          # if the number of failed detections is greater than this, dont use data
camera_center = 78/2        # center coordinate of camera
drive_power_constant = .04   # kind of like a P constant in a way, multiplied by center error to get power
drive_power_side_ratio = .75 # proportion of power to supply to other side, higher is more point turny