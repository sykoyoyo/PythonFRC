#!/usr/bin/env python3


import wpilib
import wpilib.buttons
from wpilib import RobotDrive
from robotpy_ext.common_drivers import navx

def run():
    raise ValueError()

class MyRobot(wpilib.IterativeRobot):
    
    '''Insert early definitions for Channels of Speed controls'''
    
    # Channels for the wheels
    frontLeftChannel    = 2
    rearLeftChannel     = 3
    frontRightChannel   = 1
    rearRightChannel    = 4
    
    winchMotor1        = 5
    winchMotor2        = 6
    
    # The channel on the driver station that the joystick is connected to
    # joystickChannel     = 0; <---- the semi colon comes back to haunt your code again
    joystickChannel = 0
    
    if wpilib.RobotBase.isSimulation():
            kP = 0.06
            kI = 0.00
            kD = 0.00
            kF = 0.00
        
    else:
            
            kP = 0.03
            kI = 0.00
            kD = 0.00
            kF = 0.00

    def robotInit(self):
        '''Robot initialization function - Define your inputs, and what channels they connect to'''
        
        #Which Channels are plugged into which Motor Controls for Mecanum
        #also Hack to see on SIM
        
        if not wpilib.RobotBase.isSimulation():
        
            self.FLC = ctre.CANTalon(self.rearRightChannel)
            self.FRC = ctre.CANTalon(self.rearLeftChannel)
            self.BLC = ctre.CANTalon(self.frontLeftChannel)
            self.BRC = ctre.CANTalon(self.frontRightChannel)

        else:
            self.FLC = wpilib.Talon(self.rearRightChannel)
            self.FRC = wpilib.Talon(self.rearLeftChannel)
            self.BLC = wpilib.Talon(self.frontLeftChannel)
            self.BRC = wpilib.Talon(self.frontRightChannel)
        
        #Defining Mecanum channels

        self.robotDrive = wpilib.RobotDrive(self.FLC,
                                            self.BLC,
                                            self.FRC,
                                            self.BRC)
            
        # self.robotDrive.setExpiration(0.1) <--- Don't need this when in iterative
        
        #Invert two Drive Motors for Mecanum
        
        self.robotDrive.setInvertedMotor(RobotDrive.MotorType.kFrontLeft, True)

        self.robotDrive.setInvertedMotor(RobotDrive.MotorType.kRearLeft, True)
        
        #Winch Motor Controls
        
        self.winch_motor2 = wpilib.Talon(self.winchMotor2)
        self.winch_motor1 = wpilib.Talon(self.winchMotor1)
        
        #Joystick Definition
        
        self.stick = wpilib.Joystick(self.joystickChannel)
        
        #Pneumatics Code
    
        self.fire_single_piston = wpilib.buttons.JoystickButton(self.stick, 3)
        self.fire_double_forward = wpilib.buttons.JoystickButton(self.stick, 2)
        self.fire_double_backward = wpilib.buttons.JoystickButton(self.stick, 1)
    
        self.single_solenoid = wpilib.Solenoid(1)
        self.double_solenoid = wpilib.DoubleSolenoid(2,3)
    
        #NavX Code
    
        self.sd = wpilib.SmartDashboard
        self.timer = wpilib.Timer()
        
        self.navx = navx.AHRS.create_spi()
            
        # self.analog = wpilib.AnalogInput(navx.getNavxAnalogInChannel(0)) 
        # ^^^^ we use the AHRS connection (aka putting the navx on the MXP port ontop of the RIO
                
                
    # def disablied(self): <--- wrong function name
    def disabledPeriodic(self):
    
        # Just put the yaw value into networktables as a test
        self.sd.putNumber('Yaw', self.navx.getYaw())
        
        """
        # This is sample robot stuff. You will never have a while loop in iterative
        while self.isDisabled():
    
            if self.timer.hasPeriodPassed(0.5):
                self.sd.putBoolean('SupportsDisplacement', self.navx._isDisplacementSupported())
                self.sd.putBoolean('IsCalibrating', self.navx._isCalibrating())
                self.sd.putBoolean('IsConnected', self.navx.IsConnected())
                self.sd.putNumber('Angle', self.navx.getAngle())
                self.sd.putNumber('Pitch', self.navx.getPitch())
                self.sd.putNumber('Yaw', self.navx.getYaw())
                self.sd.putNumber('roll', self.navx.getRoll())
                self.sd.putNumber('Analog', self.analog,getVoltage())
                self.sd.putNumber('Timestamp', self.navx.getLastSensorTimestamp())

            wpilib.Timer.delay(0.010)
        """
        
    def teleopInit(self):
        ''' runs Sensors and timers etc'''
        
        pass
    
    def teleopPeriodic(self):
        '''Runs the motors, Button controls, solenoids etc'''
        
            

        self.robotDrive.mecanumDrive_Cartesian(self.stick.getRawAxis(4),
                                                self.stick.getY(),
                                                self.stick.getX(), 0);
                                                   
        if self.stick.getRawButton(9):
            self.winch_motor2.set(1)
            self.winch_motor1.set(1)
        elif self.stick.getRawButton(10):
            self.winch_motor1.set(-1)
            self.winch_motor2.set(-1)
        else:
            self.winch_motor1.set(0)
            self.winch_motor2.set(0)

        if (self.fire_single_piston.get()):
            self.single_solenoid.set(True)
        else:
            self.single_solenoid.set(False)

        if (self.fire_double_forward.get()):
            self.double_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)

        elif (self.fire_double_backward.get()):
            self.double_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)


if __name__ == '__main__':
    wpilib.run(MyRobot)
