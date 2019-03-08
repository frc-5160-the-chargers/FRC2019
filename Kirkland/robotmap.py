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


# sensors
# limit switches for cargo mechanism
cargo_limit_switch_outside = 0
cargo_limit_switch_inside = 1


# these are just some constants that define robot movement
wheel_diameter = 6
encoder_ticks_per_rotation = 1024 # 1024 in 1x decoding, 4096 in 4x
encoder_wheel_geartrain_ratio = 1 # i wish it was one... find this from a mechanical :b:oi