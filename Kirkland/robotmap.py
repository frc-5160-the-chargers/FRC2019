import math

# drivetrain
# note that front is the motor towards the front, back is back, and top is the one physically above the others
left_front_drive = 5
left_top_drive = 6
left_bottom_drive = 7
right_back_drive = 4
right_top_drive = 2
right_bottom_drive = 3

# cargo device
cargo_motor = 8


#solenoids
# there are now two actuators being used to move the extension
hatch_extension_pcm = 0
hatch_extension_left_front = 4
hatch_extension_left_back = 5
hatch_extension_right_front = 6
hatch_extension_right_back = 7

shifter_pcm = 0
shifter_right_front = 3
shifter_right_back = 2
shifter_left_front = 1
shifter_left_back = 0

# these should be on a different pcm
grabber_pcm = 1
hatch_grab_front = 1
hatch_grab_back = 0


# these are just some constants that define robot movement
wheel_circumference = 6*math.pi
encoder_ticks_per_rotation = 4096 # talon srx defaults to 4096 ticks per rotation
encoder_output_shaft_ratio = 7.5 # 7.5:1 encoder shaft:output shaft
ticks_per_output_shaft_rotation = encoder_output_shaft_ratio*encoder_ticks_per_rotation
ticks_per_inch = ticks_per_output_shaft_rotation/wheel_circumference


# PID constants
# driving
drive_kP = 0.2
drive_kI = 0
drive_kD = 0
drive_buffer = 5

# turning
turn_kP = 0.1
turn_kI = 0
turn_kD = 0
turn_buffer = 5


# speed limits
# drivetrain when pid controlling
drive_pid_power_straight = .5
drive_pid_power_turn = .5


# Constants for the arduino server logic
gathering_buffer = 1       # take the last x vectors to calculate
gathering_time = 15          # if the number of failed detections is greater than this, dont use data
camera_center = 78/2        # center coordinate of camera
drive_power_constant = .02   # kind of like a P constant in a way, multiplied by center error to get power
drive_power_side_ratio = .75