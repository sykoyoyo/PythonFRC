#!/usr/bin/env python3

import wpilib # <---- main library with all the necessary code for controlling FRC robots
import wpilib.buttons # <---- for joystick buttons

class MyRobot(wpilib.IterativeRobot): # <---- IternativeRobot means that it loops over and over by itself like a while loop

    # Channels for the wheels
    topLeftChannel      = 1
    bottomLeftChannel   = 2
    topRightChannel     = 3
    bottomRightChannel  = 4
    
    leftIntakeMotor     = 5
    rightIntakeMotor    = 6

    sweeperMotor         = 11

    stage2LeftMotor     = 7
    stage2RightMotor    = 8

    stage3LeftMotor     = 9
    stage3RightMotor    = 10
    
    # The channel on the driver station that the joystick is connected to
    joystickChannelDrive    = 1
    joystickChannelShoot    = 2

    
    def robotInit(self):

        """
            Define all motor controllers, joysticks, Pneumatics, etc. here so you can use them in teleop/auton
        """

        self.robotDrive = wpilib.RobotDrive(self.topLeftChannel,
                                            self.bottomLeftChannel,
                                            self.topRightChannel,
                                            self.bottomRightChannel)
        
        self.stick = wpilib.Joystick(self.joystickChannelDrive)
        self.shooter = wpilib.Joystick(self.joystickChannelShoot)
        
        self.intakeLeft = wpilib.Talon(self.leftIntakeMotor)
        self.intakeRight = wpilib.Talon(self.rightIntakeMotor)

        self.stage2Left = wpilib.Talon(self.stage2LeftMotor)
        self.stage2Right = wpilib.Talon(self.stage2RightMotor)

        self.stage3Left = wpilib.Talon(self.stage3LeftMotor)
        self.stage3Right = wpilib.Talon(self.stage3RightMotor)

        self.sweeper = wpilib.Talon(self.sweeperMotor)


        self.shifterForward = wpilib.buttons.JoystickButton(self.stick, 2) # Xbox controller button Number 2 (B)
        self.shifterBack = wpilib.buttons.JoystickButton(self.stick, 3) # Xbox controller button Number 3 (X)

        self.double_solenoid_piston = wpilib.DoubleSolenoid(2,3) # Double Solenoid on port 2 and 3

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
#Make the robot drive there now
        self.robotDrive.arcadeDrive(self.stick, True)
            
#That there Intake looks not too shabby 
        if self.shooter.getRawButton(3):
            self.intakeLeft.set(1)
            self.intakeRight.set(-1)
            self.stage2Left.set(1)
            self.stage2Right.set(-1)
            
        elif self.shooter.getRawButton(4):
            self.intakeRight.set(1)
            self.intakeLeft.set(-1)
            self.stage2Right.set(1)
            self.stage2Left.set(-1)
            
        else:
            self.intakeLeft.set(0)
            self.intakeRight.set(0)
            self.stage2Left.set(0)
            self.stage2Right.set(0)
            
#OH SHOOT DER
        if self.shooter.getRawAxis(3):
            self.stage3Left.set(1)
            self.stage3Right.set(-1)
        elif self.shooter.getRawAxis(6):
            self.stage3Right.set(1)
            self.stage3Left.set(-1)
        else:
            self.stage3Left.set(0)
            self.stage3Right.set(0)

#Holy Shift Batman
            
        if (self.shifterForward.get()):
            self.double_solenoid_piston.set(wpilib.DoubleSolenoid.Value.kForward)

        elif (self.shifterBack.get()):
            self.double_solenoid_piston.set(wpilib.DoubleSolenoid.Value.kReverse)


            
if __name__ == "__main__":
    wpilib.run(MyRobot) #runs the code!
