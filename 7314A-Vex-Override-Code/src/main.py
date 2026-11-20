# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       ibrahimhelal, Jackson, Reid                                  #
# 	Created:      4/23/2026, 6:07:40 PM                                        #
# 	Description:  V5 project                                                   #
# Set motor stopping behavior to hold in code so the lift stays up under load. #
# ---------------------------------------------------------------------------- #

# Library imports
from token import PERCENT

from vex import * # `type: ignore

class DR4B:
    def __init__(self, left_lift_motor, right_lift_motor):
        self.left_lift_motor = left_lift_motor
        self.right_lift_motor = right_lift_motor

    def up(self):
        self.left_lift_motor.spin(FORWARD, 50, PERCENT)
        self.right_lift_motor.spin(FORWARD, 50, PERCENT)

    def down(self):
        self.left_lift_motor.spin(REVERSE, 50, PERCENT)
        self.right_lift_motor.spin(REVERSE, 50, PERCENT)

    def stop(self):
        self.left_lift_motor.stop()
        self.right_lift_motor.stop()

    #future setpoints stuff
    #def up(self):
        #self.left_lift_motor.spin_for(FORWARD, 20, DEGREES)
        #self.right_lift_motor.spin_for(FORWARD, 20, DEGREES)

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

class Claw:
    def __init__(self, motor):
        self._motor = motor

    def open(self):
        self._motor.spin(FORWARD, 100, PERCENT)

    def close(self):
        self._motor.spin(REVERSE, 100, PERCENT)

    def stop(self):
        self._motor.stop()

class Pneumatics:
    def __init__(self, pneumatics):
        self._pneumatics = pneumatics

    def open(self):
        self._pneumatics.set(True)

    def close(self):
        self._pneumatics.set(False)

class Toggle:
    def __init__(self, toggle):
        self.motor = toggle

    def turn_up(self):
        self.motor.spin(FORWARD, 100, PERCENT)

    def turn_down(self):
        self.motor.spin(REVERSE, 100, PERCENT)

    def stop(self):
        self.motor.stop()


class Robot:
    #list of all the motors ports
    #fr = Motor(Ports.PORT10) C
    #claw_motor = Motor(Ports.PORT7) 
    #fl = Motor(Ports.PORT1) C
    #bl = Motor(Ports.PORT11) C
    #br = Motor(Ports.PORT20) C
    #toggle_motor = Motor(Ports.PORT3)

    def __init__(self):
        # FR 11, FL 12, BR 8, BL 4, CLAW SWING 10, BOTTOM INTAKE 6
        #button list
        #R1 = intake in
        #L1 = swing arm fowards
        #A = claw open
        #B = claw close
        #R2 = intake out
        #L2 = swing arm backwards
        #up = open pneumatics
        #down = close pneumatics

        self.brain = Brain()
        self.controller = Controller()
        self.inertial = Inertial(Ports.PORT15)
        self.pneumatics = Pneumatics(DigitalOut(self.brain.three_wire_port.a))
        fl = Motor(Ports.PORT1, True)
        fr = Motor(Ports.PORT10, False)
        bl = Motor(Ports.PORT11, True)
        br = Motor(Ports.PORT20, False)
        self.drive_base = MecanumDrive(fl, fr, bl, br)

        self.claw = Claw(Motor(Ports.PORT2, True)) 
        self.DR4B = DR4B(Motor(Ports.PORT3, True), Motor(Ports.PORT4, False))
        self.toggle = Toggle(Motor(Ports.PORT9))
        self.pneumatics = Pneumatics(DigitalOut(self.brain.three_wire_port.a))

    def autonomous(self):
        self.brain.screen.clear_screen()
        self.brain.screen.print("autonomous code")
        # self.inertial.calibrate()
        # wait(2, SECONDS)
        self.toggle.turn_down

        # Spin the motor forward once, then reset

        self.toggle.stop
        self.toggle.spin_for(FORWARD, 360, DEGREES)
        wait(1, SECONDS)
        self.drive_base.drive_for(FORWARD, 20, INCHES)
        self.drive_base.turn_for(RIGHT, 360, DEGREES)
        # self.drive_base.turn_for(RIGHT, 90, DEGREES)
        # self.drive_base.drive_for(FORWARD, 24, INCHES)
        # self.drive_base.turn_for(RIGHT, 90, DEGREES)
        # self.drive_base.drive_for(FORWARD, 67, INCHES)

    def drive_control(self):
        fwd = self.controller.axis3.position()
        strafe = self.controller.axis4.position()
        turn = self.controller.axis1.position()
        self.drive_base.drive(fwd, strafe, turn)

    def toggle_control(self):
        # Toggle
        if(self.controller.buttonLeft.pressing()):
            self.toggle.turn_up()
        elif(self.controller.buttonRight.pressing()):
            self.toggle.turn_down()
        else:
            self.toggle.stop()

    def claw_control(self):
        # Claw
        if (self.controller.buttonA.pressing()):
            self.claw.open()
        elif (self.controller.buttonB.pressing()):
            self.claw.close()
        else:
            self.claw.stop()

    def DR4B_control(self):
        # DR4B
        if(self.controller.buttonR1.pressing()):
            self.DR4B.up()
        elif(self.controller.buttonL1.pressing()):
            self.DR4B.down()
        else:
            self.DR4B.stop()

    def show_motor_temperatures(self):
        # self.brain.screen.clear_screen()
        self.brain.screen.set_cursor(1, 1)
        self.brain.screen.print("Motor Temps:")
        self.brain.screen.set_cursor(2, 1)
        self.brain.screen.print("FL: " + str(self.drive_base.fl.temperature(TemperatureUnits.FAHRENHEIT)) + "°F | FR: " + str(self.drive_base.fr.temperature(TemperatureUnits.FAHRENHEIT)) + "°F")
        self.brain.screen.set_cursor(3, 1)
        self.brain.screen.print("BL: " + str(self.drive_base.bl.temperature(TemperatureUnits.FAHRENHEIT)) + "°F | BR: " + str(self.drive_base.br.temperature(TemperatureUnits.FAHRENHEIT)) + "°F")
        self.brain.screen.set_cursor(6, 1)
        self.brain.screen.print("Motors work well below 120°F")
        self.brain.screen.set_cursor(4, 1)
        self.brain.screen.print("bottom intake: " + str(self.conveyer_motor.conveyer_motor.temperature(TemperatureUnits.FAHRENHEIT)) + "°F") 
        self.brain.screen.set_cursor(5, 1)
        self.brain.screen.print("top intake: " + str(self.intake.half_motor.temperature(TemperatureUnits.FAHRENHEIT)) + "°F")

        # Intake Pneumatics
    
        if(self.controller.buttonUp.pressing()):
             self.pneumatics.open()
        if(self.controller.buttonDown.pressing()):
             self.pneumatics.close()

    def user_control(self):
        self.brain.screen.clear_screen()
        self.brain.screen.print("driver control")

        while True:
            self.drive_control()
            self.toggle_control()
            self.claw_control()
            self.DR4B_control()
            self.show_motor_temperatures()

rollingrobot = Robot()

def autonomous():
    rollingrobot.autonomous()

def user_control():
    rollingrobot.user_control()

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
rollingrobot.brain.screen.clear_screen()
