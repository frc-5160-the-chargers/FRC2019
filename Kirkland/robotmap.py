# robotmap.py
# pretty much all of the robot configuration
# note the class structure, this makes it easier to access things without having really long and confusing variable names

from wpilib import DoubleSolenoid
from ctre import NeutralMode


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

    class PressureSensor:
        port = 1


class Physics:
    class Drivetrain:
        diameter = 6  # inches
        circumference = diameter * 3.14

        ticks_per_rotation = 4096  # talon srx default
        output_shaft_ratio = 7.5  # for every 7.5 encoder rotations, the output shaft turns once

        ticks_per_output_rotation = ticks_per_rotation * output_shaft_ratio
        ticks_per_inch = ticks_per_output_rotation / circumference

    class PressureSensor:
        calibration_pressure = 112


class Tuning:
    class Drivetrain:
        motor_power_percentage_limit = .5

        min_shifting_speed = 5
        shifting_speed_enabled = False

        drive_straight_constant = .01

        class Shifters:
            low_gear_state = DoubleSolenoid.Value.kForward
            high_gear_state = DoubleSolenoid.Value.kReverse

    class CargoMechanism:
        deadzone = 0.1

        class Rotator:
            lifting_power_limit = .25
            lowering_power_limit = .2

        class Servo:
            locked_position = 180
            unlocked_position = 0

    class HatchMechanism:
        class Grabber:
            grabbing_state = DoubleSolenoid.Value.kForward
            released_state = DoubleSolenoid.Value.kReverse

        class Rack:
            extended_state = DoubleSolenoid.Value.kForward
            retracted_state = DoubleSolenoid.Value.kReverse


class MotorConfiguration:
    class Drivetrain:
        peak_current = 30
        peak_current_duration = 5
        neutral_mode = NeutralMode.Coast
        ramp_rate = 0.3

    class Cargo:
        pass
