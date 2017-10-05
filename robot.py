#!/usr/bin/env python3


import wpilib
import wpilib.buttons
from wpilib import RobotDrive
from robotpy_ext.common_drivers import navx


class MyRobot(wpilib.IterativeRobot):
    
    '''Insert early definitions for Channels of Speed controls'''
    
    # Channels for the wheels
    frontLeftChannel    = 3
    rearLeftChannel     = 2
    frontRightChannel   = 4
    rearRightChannel    = 1
    
    winchMotor1        = 7
    winchMotor2        = 8
    
    # The channel on the driver station that the joystick is connected to
    joystickChannel     = 0
    
    def robotInit(self):
        '''Robot initialization function - Define your inputs, and what channels they connect to'''
        
        #Which Channels are plugged into which Motor Controls for Mecanum
        #also Hack to see on SIM
        
        if not wpilib.RobotBase.isSimulation():
            import ctre
        
            self.BRC = ctre.CANTalon(self.rearRightChannel)
            self.BLC = ctre.CANTalon(self.rearLeftChannel)
            self.FLC = ctre.CANTalon(self.frontLeftChannel)
            self.FRC = ctre.CANTalon(self.frontRightChannel)

        else:
            self.BRC = wpilib.Talon(self.rearRightChannel)
            self.BLC = wpilib.Talon(self.rearLeftChannel)
            self.FLC = wpilib.Talon(self.frontLeftChannel)
            self.FRC = wpilib.Talon(self.frontRightChannel)
        
        #Defining Mecanum channels

        self.robotDrive = wpilib.RobotDrive(self.FLC,
                                            self.BLC,
                                            self.FRC,
                                            self.BRC)
            
        self.robotDrive.setExpiration(0.1)
        
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
    


    
    def teleopInit(self):
        ''' runs Sensors and timers etc'''
        
        pass
    
    def teleopPeriodic(self):
        '''Runs the motors, Button controls, solenoids etc'''
        
            
        #Drive Command
        self.robotDrive.mecanumDrive_Cartesian(self.stick.getRawAxis(4), self.stick.getY(), self.stick.getX(), 0)
        
        #Winch Buttons
        if self.stick.getRawButton(5):
                self.winch_motor2.set(1)
                self.winch_motor1.set(1)
        elif self.stick.getRawButton(6):
                self.winch_motor1.set(-1)
                self.winch_motor2.set(-1)
        else:
                self.winch_motor1.set(0)
                self.winch_motor2.set(0)
        
        #Flipper for gear intake
        if (self.fire_single_piston.get()):
            self.single_solenoid.set(True)
        else:
            self.single_solenoid.set(False)
        
        #Open/Close Gear placer
        if (self.fire_double_forward.get()):
            self.double_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)

        elif (self.fire_double_backward.get()):
            self.double_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)


if __name__ == '__main__':
    wpilib.run(MyRobot)
