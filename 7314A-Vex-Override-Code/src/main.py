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

fl_motor = Motor(Ports.PORT20)
fr_motor = Motor(Ports.PORT12)
br_motor = Motor(Ports.PORT1)  
bl_motor = Motor(Ports.PORT3)

my_robot = MecanumDrive(fl_motor, fr_motor, bl_motor, br_motor)

brain = Brain()

my_robot.drive(50, 50, 50)  # Drive forward at 50% speed