# utils.py
# standard utilities and functions that aren't in the python stl for some reason

import ctre
import robotmap


def clamp(i, minNum, maxNum):
    # clamp a number between a min and a max
    return max(min(i, maxNum), minNum)


def configure_motor(motor: ctre.WPI_TalonSRX, neutral_mode: ctre.NeutralMode, peak_current=0, peak_current_duration=0, ramp_rate=0):
    # motor.configFactoryDefault()
    motor.clearStickyFaults()
    motor.setNeutralMode(neutral_mode)
    if peak_current != 0:
        motor.enableCurrentLimit(True)
        motor.configPeakCurrentLimit(peak_current)
        motor.configPeakCurrentDuration(peak_current_duration)
    else:
        motor.enableCurrentLimit(False)
    if ramp_rate != 0:
        motor.configOpenLoopRamp(ramp_rate)


def configure_drivetrain_motors(*args):
    for _, motor in enumerate(args):
        configure_motor(motor, robotmap.MotorConfiguration.Drivetrain.neutral_mode, robotmap.MotorConfiguration.Drivetrain.peak_current,
                        robotmap.MotorConfiguration.Drivetrain.peak_current_duration, robotmap.MotorConfiguration.Drivetrain.ramp_rate)
