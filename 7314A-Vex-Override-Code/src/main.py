# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       ibrahimhelal, Jackson, Amir, Bruno                           #
# 	Created:      4/23/2026, 6:07:40 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

class Intake:
    def __init__(self, left_motor, right_motor):
        self._left_motor = left_motor
        self._right_motor = right_motor

    def spin(self):
        # Code to intake
        self._left_motor.spin(FORWARD, 100, PERCENT)
        self._right_motor.spin(REVERSE, 100, PERCENT)

class MecanumDrive:
    def __init__(self, fl, fr, bl, br):
        self.fl = fl
        self.fr = fr
        self.bl = bl
        self.br = br
        left = MotorGroup(fl, bl)
        right = MotorGroup(fr, br)
        self._drivetrain = DriveTrain(left, right, 319.19, 295, 130, MM, 1.0)

    def drive(self, fwd, strafe, turn):
        fl_speed = fwd + strafe + turn
        fr_speed = fwd - strafe - turn
        bl_speed = fwd - strafe + turn
        br_speed = fwd + strafe - turn
        self.fl.spin(FORWARD, fl_speed, PERCENT)
        self.fr.spin(FORWARD, fr_speed, PERCENT)
        self.bl.spin(FORWARD, bl_speed, PERCENT)
        self.br.spin(FORWARD, br_speed, PERCENT)

    def drive_for(self, direction, distance, unit):
        self._drivetrain.drive_for(direction, distance, unit)

    def turn_for(self, direction, angle, unit):
        self._drivetrain.turn_for(direction, angle, unit)


class Robot:
    def __init__(self):
        self.brain = Brain()
        self.controller = Controller()
        self.inertial = Inertial(Ports.PORT15)

        
        fl = Motor(Ports.PORT1, False)
        fr = Motor(Ports.PORT10, True)
        bl = Motor(Ports.PORT11, False)
        br = Motor(Ports.PORT20, True)
        self.drive_base = MecanumDrive(fl, fr, bl, br)

        l_intake_motor = Motor(Ports.PORT5)
        r_intake_motor = Motor(Ports.PORT6)
        self.intake = Intake(l_intake_motor, r_intake_motor)

    def autonomous(self):
        self.brain.screen.clear_screen()
        self.brain.screen.print("autonomous code")
        self.inertial.calibrate()
        wait(2, SECONDS)
        self.drive_base.drive_for(FORWARD, 24, INCHES)
        self.drive_base.turn_for(RIGHT, 90, DEGREES)
        self.drive_base.drive_for(FORWARD, 24, INCHES)
        self.drive_base.turn_for(RIGHT, 90, DEGREES)
        self.drive_base.drive_for(FORWARD, 67, INCHES)

    def user_control(self):
        self.brain.screen.clear_screen()
        self.brain.screen.print("driver control")
        while True:
            fwd = self.controller.axis3.position()
            strafe = self.controller.axis4.position()
            turn = self.controller.axis1.position()
            self.drive_base.drive(fwd, strafe, turn)

            # Check if R1 is pressed
            move_intake_pressed = self.controller.buttonR1.pressing

            if (move_intake_pressed):
                self.intake.spin()

            wait(1, MSEC)


space_ship = Robot()

def autonomous():
    space_ship.autonomous()

def user_control():
    space_ship.user_control()

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
space_ship.brain.screen.clear_screen()
