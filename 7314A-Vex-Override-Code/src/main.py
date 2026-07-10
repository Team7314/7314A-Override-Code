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
from vex import Motor, FORWARD, PERCENT, Ports


class MecanumDrive:
    def __init__(self, fl_motor, fr_motor, bl_motor, br_motor):
        self.controller = Controller()
        self.inertial_sensor = Inertial(Ports.PORT15)

    def update_display_color(self):
        color = self.pin_color_sensor.color()
        if color == Color.RED:
            self.brain.screen.set_fill_color(Color.RED)
            self.brain.screen.draw_rectangle(0, 0, 480, 240)
        elif color == Color.YELLOW:
            self.brain.screen.set_fill_color(Color.YELLOW)
            self.brain.screen.draw_rectangle(0, 0, 480, 240)
        elif color == Color.BLUE:
            self.brain.screen.set_fill_color(Color.BLUE)
            self.brain.screen.draw_rectangle(0, 0, 480, 240)
        else:
            self.brain.screen.set_fill_color(Color.BLACK)
            self.brain.screen.draw_rectangle(0, 0, 480, 240)

    def autonomous(self):
        self.brain.screen.clear_screen()
        self.brain.screen.print("autonomous code")

        # place automonous code here
        Inertial(Ports.PORT2).calibrate()
        wait(2, SECONDS)
        DriveTrain(Ports.PORT1, Ports.PORT10, Ports.PORT11, Ports.PORT20).drive_for(FORWARD, 24, INCHES)
        DriveTrain(Ports.PORT1, Ports.PORT10, Ports.PORT11, Ports.PORT20).turn_for(FORWARD, 0, DEGREES, 90, PERCENT, True)
        DriveTrain(Ports.PORT1, Ports.PORT10, Ports.PORT11, Ports.PORT20).drive_for(FORWARD, 24, INCHES)
        DriveTrain(Ports.PORT1, Ports.PORT10, Ports.PORT11, Ports.PORT20).turn_for(FORWARD, 0, DEGREES, 90, PERCENT, True)
        DriveTrain(Ports.PORT1, Ports.PORT10, Ports.PORT11, Ports.PORT20).drive_for(FORWARD, 67, INCHES)

    def user_control(self):
        self.brain.screen.clear_screen()
        self.brain.screen.print("driver control")
        # place driver control in this while loop

        while True:
            fwd = self.controller.axis3.position()
            strafe = self.controller.axis4.position()
            turn = self.controller.axis1.position()
            self.drive_base.drive(fwd, strafe, turn)

            self.update_display_color()
            
            wait(1, MSEC)

        # place automonous code here
<<<<<<< HEAD
>>>>>>> 8a42928 (Added color sensor)
=======
Inertial(Ports.PORT2).calibrate()
wait(2, SECONDS)
self.drive_base.drive_for(FORWARD, 34, INCHES)
self.drive_base.turn_for(LEFT, 90, DEGREES)
self.drive_base.drive_for(FORWARD, 57, INCHES)
self.drive_base.turn_for(RIGHT, 90, DEGREES)
self.drive_base.drive_for(FORWARD, 52, INCHES)
self.drive_base.turn_for(RIGHT, 90, DEGREES)
self.drive_base.drive_for(FORWARD, 57, INCHES)
self.drive_base.turn_for(RIGHT, 90, DEGREES)
self.drive_base.drive_for(FORWARD, 28, INCHES)
self.drive_base.turn_for(RIGHT, 90, DEGREES)
self.drive_base.drive_for(FORWARD, 22, INCHES)
        
        
>>>>>>> 6b1dae3 (Added auton code)
    
def user_control(self):
    self.brain.screen.clear_screen()
    self.brain.screen.print("driver control")
        # place driver control in this while loop


    while True:
        fwd = self.controller.axis3.position()
        strafe = self.controller.axis4.position()
        turn = self.controller.axis1.position()
        self.drive_base.drive(fwd, strafe, turn)

        self.update_display_color()
            
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
