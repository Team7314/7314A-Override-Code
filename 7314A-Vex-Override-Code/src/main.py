# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       ibrahimhelal, Jackson, Amir, Bruno                                        #
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
        self.brain = Brain()
        # self.pin_color_sensor = ColorSensor(Ports.PORT3)  # Color sensor not available in vex module
        self.drive_base = DriveTrain(fl_motor, fr_motor, bl_motor, br_motor)

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
            self.drive_base.drive(FORWARD, fwd, PERCENT)

            self.update_display_color()
            
            wait(1, MSEC)


class Robot:
    def __init__(self):
        self.mecanum_drive = MecanumDrive(Ports.PORT1, Ports.PORT10, Ports.PORT11, Ports.PORT20)
    
    def autonomous(self):
        self.mecanum_drive.autonomous()
    
    def user_control(self):
        self.mecanum_drive.user_control()


robot = Robot()

def autonomous():
    robot.autonomous()

def user_control():
    robot.user_control()

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
robot.mecanum_drive.brain.screen.clear_screen()
