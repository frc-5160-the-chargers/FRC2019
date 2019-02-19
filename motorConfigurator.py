import ctre

class MotorConfigurator:
    @staticmethod
    def configure_drivetrain_cim(motor: ctre.WPI_TalonSRX):
        """
        Configure a given motor controller for drivetrain usage
            :param motor:ctre.WPI_TalonSRX: The motor to be configured
        """
        # 0 is disabled for ramp rates, input is in seconds
        motor.configOpenLoopRamp(0)
        motor.configClosedLoopRamp(0)

    @staticmethod
    def bulk_config_drivetrain(*args):
        """
        Calls the drivetrain configuration function on all motors passed to this function
            :param *args: The motors to be configured
        """
        for _, motor in enumerate(args):
            MotorConfigurator.configure_drivetrain_cim(motor)