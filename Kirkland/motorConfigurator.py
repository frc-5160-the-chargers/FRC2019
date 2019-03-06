import ctre

class MotorConfigurator:
    @staticmethod
    def configure_drivetrain_cim(motor: ctre.WPI_TalonSRX):
        """
        Configure a given motor controller for drivetrain usage
            :param motor:ctre.WPI_TalonSRX: The motor to be configured
        """
        # motor.configFactoryDefault()
        # 0 is disabled for ramp rates, input is in seconds
        motor.configOpenLoopRamp(0.5)
        motor.clearStickyFaults()
        motor.enableCurrentLimit(True)
        motor.configContinuousCurrentLimit(70)
        motor.configPeakCurrentLimit(0)
        motor.setNeutralMode(ctre.NeutralMode.Brake)

    @staticmethod
    def bulk_config_drivetrain(*args):
        """
        Calls the drivetrain configuration function on all motors passed to this function
            :param *args: The motors to be configured
        """
        for _, motor in enumerate(args):
            MotorConfigurator.configure_drivetrain_cim(motor)