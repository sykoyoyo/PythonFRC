#!/usr/bin/env python3


import wpilib
import wpilib.buttons
from wpilib import RobotDrive
import networktables
from robotpy_ext.common_drivers import navx


class MyRobot(wpilib.IterativeRobot):
    
    '''Insert early definitions for Channels of Speed controls'''
    
    # Channels for the wheels and motors
    frontLeftChannel    = 2
    rearLeftChannel     = 3
    frontRightChannel   = 1
    rearRightChannel    = 0
    
    winchMotor1        = 4
    winchMotor2        = 5
    
    # The channel on the driver station that the joystick is connected to
    joystickChannel     = 0;
    
    def robotInit(self):
        '''Robot initialization function - Define your inputs, and what channels they connect to'''

        self.robotDrive = wpilib.RobotDrive(self.frontLeftChannel,
                                            self.rearLeftChannel,
                                            self.frontRightChannel,
                                            self.rearRightChannel)
            
        self.robotDrive.setExpiration(0.1)

        self.robotDrive.setInvertedMotor(RobotDrive.MotorType.kFrontLeft, True)

        self.robotDrive.setInvertedMotor(RobotDrive.MotorType.kRearLeft, True)

        self.winch_motor2 = wpilib.Talon(self.winchMotor2)
        self.winch_motor1 = wpilib.Talon(self.winchMotor1)
        
        self.stick = wpilib.Joystick(self.joystickChannel)
        
        self.fire_single_piston = wpilib.buttons.JoystickButton(self.stick, 1)
        self.fire_double_forward = wpilib.buttons.JoystickButton(self.stick, 2)
        self.fire_double_backward = wpilib.buttons.JoystickButton(self.stick, 3)
    
        self.single_solenoid = wpilib.Solenoid(1)
        self.double_solenoid = wpilib.DoubleSolenoid(2,3)
    
    def autonomousInit(self):
        '''Runs once each time the robot enters in Auto Mode'''

        self.auto_loop_counter = 0
    
    def autonomousPeriodic(self):
        '''called periodically during Autonomous'''
        
        if self.auto_loop_counter < 100:
            self.robotDrive.drive(-0.5, 0)
            self.auto_loop_counter +=1
        else:
            self.robotDrive.drive(0,0)


    def teleopInit(self):
        ''' runs Sensors and timers etc'''
        
        pass
    
    def teleopPeriodic(self):
        '''Runs the motors, Button controls, solenoids etc'''
        
            

        self.robotDrive.mecanumDrive_Cartesian(self.stick.getRawAxis(4),
                                                self.stick.getY(),
                                                self.stick.getX(), 0);
                                                   
        if self.stick.getRawButton(3):
                self.winch_motor2.set(1)
                self.winch_motor1.set(1)
        elif self.stick.getRawButton(4):
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


    def testPeriodic(self):
            '''Function called periodically during Test Mode'''
        wpilib.LiveWindow.run()

if __name__ == '__main__':
    wpilib.run(MyRobot)
