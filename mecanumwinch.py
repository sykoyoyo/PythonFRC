#!/usr/bin/env python3

import wpilib # <---- main library with all the necessary code for controlling FRC robots
import wpilib.buttons # <---- for joystick buttons

class MyRobot(wpilib.IterativeRobot): # <---- IternativeRobot means that it loops over and over by itself like a while loop

    # Channels for the wheels
    frontLeftChannel    = 2
    rearLeftChannel     = 3
    frontRightChannel   = 1
    rearRightChannel    = 0
    
    winchMotor1        = 4
    winchMotor2        = 5
    
    # The channel on the driver station that the joystick is connected to
    joystickChannel     = 0
    
    def robotInit(self):

        """
            Define all motor controllers, joysticks, Pneumatics, etc. here so you can use them in teleop/auton
        """

        self.robotDrive = wpilib.RobotDrive(self.frontLeftChannel,
                                            self.rearLeftChannel,
                                            self.frontRightChannel,
                                            self.rearRightChannel)

        self.robotDrive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontLeft, True)

        self.robotDrive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearLeft, True)
        
        self.winch_motor2 = wpilib.Talon(self.winchMotor2)
        self.winch_motor1 = wpilib.Talon(self.winchMotor1)
        
        self.stick = wpilib.Joystick(self.joystickChannel)


    def teleopInit(self):

        """
            Put code in here that you want ran once before teleop starts.
            I use it for timers and counters.
        """
        pass

    def teleopPeriodic(self):

        """
            Human controlled period
        """
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
        
if __name__ == "__main__":
    wpilib.run(MyRobot) #runs the code!
