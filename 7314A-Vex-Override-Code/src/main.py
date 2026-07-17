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
            wait(1, MSEC)


robot = Robot()

def autonomous():
    robot.autonomous()

def user_control():
    robot.user_control()

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
robot.brain.screen.clear_screen()
