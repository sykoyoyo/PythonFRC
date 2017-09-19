#!/usr/bin/env python3
'''
    This is a demo program showing how to use Mecanum control with the
    RobotDrive class.
    '''

import wpilib
from wpilib import RobotDrive

class MyRobot(wpilib.IterativeRobot):
    
    # Channels for the wheels
    frontLeftChannel    = 2
    rearLeftChannel     = 3
    frontRightChannel   = 1
    rearRightChannel    = 0
    
    winchMotor1        = 4
    winchMotor2        = 5
    
    # The channel on the driver station that the joystick is connected to
    joystickChannel     = 0;
    
    def robotInit(self):
        '''Robot initialization function'''

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
    
    def teleopInit(self):
        ''' runs Sensors and timers etc'''
        
        pass
    
    def teleopPeriodic(self):
        '''Runs the motors with Mecanum drive.'''
        
            

        self.robotDrive.mecanumDrive_Cartesian(self.stick.getX(),
                                                self.stick.getY(),
                                                self.stick.getRawAxis(5), 0);
                                                   
        if self.stick.getRawButton(3):
                self.winch_motor2.set(1)
                self.winch_motor1.set(1)
        elif self.stick.getRawButton(4):
                self.winch_motor1.set(-1)
                self.winch_motor2.set(-1)
        else:
                self.winch_motor1.set(0)
                self.winch_motor2.set(0)
                                                   
        wpilib.Timer.delay(0.005)



if __name__ == '__main__':
    wpilib.run(MyRobot)
