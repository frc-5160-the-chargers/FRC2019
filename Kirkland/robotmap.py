class Ports:
    class Drivetrain:
        class Motors:
            left_front = 5
            left_top = 6
            left_bottom = 7

            right_back = 4
            right_top = 2
            right_bottom = 3

        class Shifters:
            pcm = 0

            left_front = 1
            left_back = 0

            right_front = 3
            right_back = 2
    
    class Cargo:
        rotator = 8

        locking_servo = 0

    class Hatch:
        class Extension:
            pcm = 0

            left_front = 4
            left_back = 5

            right_front = 6
            right_back = 7
        
        class Grabber:
            pcm = 1
            
            front = 1
            back = 0
    
class Physics:
    class Drivetrain:
        class Wheels:
            diameter = 6 # inches
            circumference = diameter * 3.14
        
        class Encoders:
            ticks_per_rotation = 4096 # talon srx default
            output_shaft_ratio = 7.5  # for every 7.5 encoder rotations, the output shaft turns once
            
            ticks_per_output_rotation = ticks_per_rotation * output_shaft_ratio
            ticks_per_inch = ticks_per_output_rotation / Wheels.circumference

class Tuning:
    class PID:
        pass

    class Limits:
        drivetrain_power_limit = .5

class Cameras:
    cargo_name = "cargo camera"
    cargo_dev_address = "/dev/v4l/by-path/platform-ci_hdrc.0-usb-0:1.2.2:1.0-video-index0"

    hatch_name = "hatch camera"
    hatch_dev_address = "/dev/v4l/by-path/platform-ci_hdrc.0-usb-0:1.2.3:1.0-video-index0"

    front_name = "front camera"
    front_dev_address = "/dev/v4l/by-path/platform-ci_hdrc.0-usb-0:1.2.4:1.0-video-index0"