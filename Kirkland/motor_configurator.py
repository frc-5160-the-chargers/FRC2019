import ctre

def configure_cargo_redline(motor: ctre.WPI_TalonSRX):
    """
    Configure a given motor controller for drivetrain usage
        :param motor:ctre.WPI_TalonSRX: The motor to be configured
    """
    # motor.configFactoryDefault()
    # 0 is disabled for ramp rates, input is in seconds
    motor.clearStickyFaults()
    motor.setNeutralMode(ctre.NeutralMode.Brake)

def configure_drivetrain_cim(motor: ctre.WPI_TalonSRX):
    """
    Configure a given motor controller for drivetrain usage
        :param motor:ctre.WPI_TalonSRX: The motor to be configured
    """
    # motor.configFactoryDefault()
    # 0 is disabled for ramp rates, input is in seconds
    # TODO: 30 amp over 5 seconds in the future
    motor.configOpenLoopRamp(0.3)
    motor.clearStickyFaults()
    motor.enableCurrentLimit(True)
    motor.configContinuousCurrentLimit(70)
    motor.configPeakCurrentLimit(0)
    motor.setNeutralMode(ctre.NeutralMode.Brake)

def bulk_config_drivetrain(*args):
    """
    Calls the drivetrain configuration function on all motors passed to this function
        :param *args: The motors to be configured
    """
    for _, motor in enumerate(args):
        configure_drivetrain_cim(motor)