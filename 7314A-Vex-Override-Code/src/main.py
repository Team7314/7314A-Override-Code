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
    def __init__(self):
        self.brain = Brain()
        self.controller = Controller()
        self.drive_base = DriveTrain(Ports.PORT1, Ports.PORT10, Ports.PORT11, Ports.PORT20)
        self.inertial_sensor = Inertial(Ports.PORT2)
        self.pin_color_sensor = None

        try:
            self.pin_color_sensor = ColorSensor(Ports.PORT3)
        except Exception:
            self.pin_color_sensor = None

    def update_display_color(self):
        if self.pin_color_sensor is None:
            self.brain.screen.set_fill_color(Color.BLACK)
            self.brain.screen.draw_rectangle(0, 0, 480, 240)
            return

        color = self.pin_color_sensor.color()
        if color == Color.RED:
            fill = Color.RED
        elif color == Color.YELLOW:
            fill = Color.YELLOW
        elif color == Color.BLUE:
            fill = Color.BLUE
        else:
            fill = Color.BLACK

        self.brain.screen.set_fill_color(fill)
        self.brain.screen.draw_rectangle(0, 0, 480, 240)

    def autonomous(self):
        self.brain.screen.clear_screen()
        self.brain.screen.print("autonomous code")

        self.inertial_sensor.calibrate()
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

            self.update_display_color()
            wait(1, MSEC)


robot = MecanumDrive()


def autonomous():
    robot.autonomous()


def user_control():
    robot.user_control()


# create competition instance
comp = Competition(autonomous, user_control)


# actions to do when the program starts
robot.brain.screen.clear_screen()
