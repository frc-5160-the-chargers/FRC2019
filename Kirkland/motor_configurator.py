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
    motor.configContinuousCurrentLimit(30)
    motor.configPeakCurrentLimit(0)
    motor.setNeutralMode(ctre.NeutralMode.Brake)

def configure_motor_coast(motor : ctre.WPI_TalonSRX):
    """
    make a motor set to coast
    """
    motor.setNeutralMode(ctre.NeutralMode.Coast)

def bulk_config_drivetrain(*args):
    """
    Calls the drivetrain configuration function on all motors passed to this function
        :param *args: The motors to be configured
    """
    for _, motor in enumerate(args):
        configure_drivetrain_cim(motor)

def bulk_config_drivetrain_coast(*args):
    """
    set all motors to coast
    """
    for _, motor in enumerate(args):
        configure_motor_coast(motor)