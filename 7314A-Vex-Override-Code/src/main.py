# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       ibrahimhelal                                                 #
# 	Created:      4/23/2026, 6:07:40 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
from vex import Motor, FORWARD, PERCENT, Ports


class MecanumDrive:
    def __init__(self, fl_motor, fr_motor, bl_motor, br_motor):
        self.fl_motor : Motor = fl_motor
        self.fr_motor : Motor = fr_motor
        self.bl_motor : Motor = bl_motor
        self.br_motor : Motor = br_motor
        
    def drive(self, fwd, strafe, turn):        
        fl = fwd + strafe + turn
        fr = fwd - strafe - turn
        bl = fwd - strafe + turn
        br = fwd + strafe - turn
        
        top_speed = max(abs(fl), abs(fr), abs(bl), abs(br), 100)
        scale = 100.0 / top_speed
        
        self.fl_motor.spin(FORWARD, -(fl * scale), PERCENT)
        self.fr_motor.spin(FORWARD, (fr * scale), PERCENT)
        self.bl_motor.spin(FORWARD, -(bl * scale), PERCENT)
        self.br_motor.spin(FORWARD, (br * scale), PERCENT)


class Robot:
    def __init__(self):
        self.brain = Brain()
        fl_motor = Motor(Ports.PORT1)
        fr_motor = Motor(Ports.PORT10)
        br_motor = Motor(Ports.PORT20)  
        bl_motor = Motor(Ports.PORT11)
        self.pin_color_sensor = Optical(Ports.PORT15)
        self.drive_base = MecanumDrive(fl_motor, fr_motor, bl_motor, br_motor)
        self.pin_color_sensor.set_light_power(100, PERCENT)
        self.controller = Controller()
    
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
