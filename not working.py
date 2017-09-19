#!/usr/bin/env python3

import wpilib
import wpilib.buttons
from wpilib import RobotDrive

class MyRobot(wpilib.IterativeRobot):
    
    
    
    frontLeftChannel    = 2
    rearLeftChannel     = 3
    frontRightChannel   = 1
    rearRightChannel    = 0
    
    jotstickChannel     = 0;
    

    def robotInit(self):

        """
            Define all motor controllers, joysticks, Pneumatics, etc. here so you can usem in teleop/auton.

        """

        self.drive_motor1 = wpilib.Talon(0)
        self.drive_motor2 = wpilib.Talon(1)
        self.drive_motor3 = wpilib.Talon(2)
        self.drive_motor4 = wpilib.Talon(3)
        
        self.winch_motor1 = wpilib.Talon(5)
        self.winch_motor2 = wpilib.Talon(6)
        
        self.mecDrive = wpilib.RobotDrive(self.frontLeftChannel,
                                          self.rearLeftChannel,
                                          self.frontRightChannel,
                                          self.rearRightChannel)

        self.mecDrive.setExpiration(0.1)
        
        self.mecDrive.setInvertedMotor(RobotDrive.MotorType.kFrontLeft, True)
        self.mecDrive.setInvertedMotor(RobotDrive.MotorType.kRearLeft, True)
        
        
        self.robot_Drive = wpilib.RobotDrive(self.drive_motor1, self.drive_motor2)

        self.xbox = wpilib.Joystick(0)

        self.forwardWinch = wpilib.buttons.JoystickButton(self.xbox, 3)
        self.reverseWinch = wpilib.buttons.JoystickButton(self.xbox, 2)

        


    def teleopInit(self):

        """
            Put Code in here that you want to run for Teleop
            Timers, Counters etc
        """
        pass

    def teleopPeriodic(self):

        """
            Human Controlled Period

        """

        
        

        self.mecDrive.setSafetyEnabled(True)
        while self.isOperatorControl() and self.isEnabled():
            self.mecDrive.mecanumDrive_Cartesian(self.xbox.getX(),
                                                 self.xbox.getY(),
                                                 self.xbox.getZ(), 0);
                                                 
            wpilib.Timer.delay(0.005)
        
        if (self.forwardWinch.get()):
            self.winch_motor1.set(1)
            self.winch_motor2.set(1)
        else:
            self.winch_motor1.set(0)
            self.winch_motor2.set(0)

        if (self.reverseWinch.get()):
            self.winch_motor1.set(-1)
            self.winch_motor2.set(-1)
        else:
            self.winch_motor1.set(0)
            self.winch_motor2.set(0)
            
if __name__ == "__main__":
    wpilib.run(MyRobot)
    
        
