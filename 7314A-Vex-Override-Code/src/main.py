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

    def in_take(self):
        # Code to intake
        self._left_motor.spin(FORWARD, 100, PERCENT)
        self._right_motor.spin(REVERSE, 100, PERCENT)

    def out_take(self):
        # Code to intake
        self._left_motor.spin(FORWARD, -100, PERCENT)
        self._right_motor.spin(REVERSE, -100, PERCENT)

    def stop(self):
        # Code to intake
        self._left_motor.stop()
        self._right_motor.stop()

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

class Swingarm:
    def __init__(self, turnmotor):
        self._motor = turnmotor

    def fowards(self):
        self._motor.spin(FORWARD, 100, PERCENT)

    def backwards(self):
        self._motor.spin(REVERSE, 100, PERCENT)

    def stop(self):
        self._motor.stop()

class Pneumatics:
    def __init__(self, pneumatics):
        self._pneumatics = pneumatics

    def open(self):
        v5pneumatics.open()

    def close(self):
        v5pneumatics.close()

class Lift:
    def __init__(self, liftmotor):
        self._motor = liftmotor

    def up(self):
        self._motor.spin(FORWARD, 100, PERCENT)

    def down(self):
        self._motor.spin(REVERSE, 100, PERCENT)

    def stop(self):
        self._motor.stop()


    class conveyor:
        def __init__(self, conveyormotor):
            self._motor = conveyormotor

        def up(self):
            self._motor.spin(FORWARD, 100, PERCENT)

        def down(self):
            self._motor.spin(REVERSE, 100, PERCENT)

        def stop(self):
            self._motor.stop()

class Toggle:
    def __init__(self, toggle):
        self._motor = toggle

    def turn_up(self):
        self._motor.spin(FORWARD, 100, PERCENT)

    def turn_down(self):
        self._motor.spin(REVERSE, 100, PERCENT)

    def stop(self):
        self._motor.stop()


class Robot:
    #list of all the motors ports
    #fr = Motor(Ports.PORT4) C
    #conveyor_motor = Motor(Ports.PORT6) C
    #claw_motor = Motor(Ports.PORT7) 
    #fl = Motor(Ports.PORT8) C
    #intake_motor = Motor(Ports.PORT9) C
    #swing_arm = Motor(Ports.PORT10) C
    #bl = Motor(Ports.PORT11) C
    #br = Motor(Ports.PORT12) C
    #lift_motor = Motor(Ports.PORT2)
    #toggle_motor = Motor(Ports.PORT3)

    def __init__(self):
        # FR 11, FL 12, BR 8, BL 4, CLAW SWING 10, BOTTOM INTAKE 6
        #button list
        #R1 = intake in
        #L1 = intake out
        #A = claw open
        #B = claw close
        #R2 = swing arm fowards
        #L2 = swing arm backwards
        #up = open pneumatics
        #down = close pneumatics

        self.brain = Brain()
        self.controller = Controller()
        self.inertial = Inertial(Ports.PORT15)
        fl = Motor(Ports.PORT12, True)
        fr = Motor(Ports.PORT11, False)
        bl = Motor(Ports.PORT4, True)
        br = Motor(Ports.PORT8, False)
        self.drive_base = MecanumDrive(fl, fr, bl, br)

        # intake_motor = Motor(Ports.PORT5, False)
        # self.intake = Intake(intake_motor)

        self.claw = Claw(Motor(Ports.PORT10, True))
        self.swing_arm = Swingarm(Motor(Ports.PORT10))
        # self.lift = Lift(Motor(Ports.PORT20))
        self.toggle = Toggle(Motor(Ports.PORT9))

    def autonomous(self):
        self.brain.screen.clear_screen()
        self.brain.screen.print("autonomous code")
        # self.inertial.calibrate()
        # wait(2, SECONDS)
        self.drive_base.drive_for(FORWARD, 20, INCHES)
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

    def swing_arm_control(self):
        # Swing Arm
        if (self.controller.buttonR2.pressing()):
            self.swing_arm.fowards()
        elif (self.controller.buttonL2.pressing()):
            self.swing_arm.backwards()
        else:
            self.swing_arm.stop()

    def show_motor_temperatures(self):
        # self.brain.screen.clear_screen()
        self.brain.screen.set_cursor(1, 1)
        self.brain.screen.print("Motor Temps:")
        self.brain.screen.set_cursor(2, 1)
        self.brain.screen.print("FL: " + str(self.drive_base.fl.temperature(TemperatureUnits.CELSIUS)) + "°C | FR: " + str(self.drive_base.fr.temperature(TemperatureUnits.CELSIUS)) + "°C")
        self.brain.screen.set_cursor(3, 1)
        self.brain.screen.print("BL: " + str(self.drive_base.bl.temperature(TemperatureUnits.CELSIUS)) + "°C | BR: " + str(self.drive_base.br.temperature(TemperatureUnits.CELSIUS)) + "°C")
        self.brain.screen.set_cursor(4, 1)
        self.brain.screen.print("Motors work well below 55°C")


    # def lift_control(self):
    #     # Lift
    #     if(self.controller.buttonR2.pressing()):
    #         self.lift.up()
    #     elif(self.controller.buttonL2.pressing()):
    #         self.lift.down()
    #     else:
    #         self.lift.stop()

    # def intake_control(self):
        # Intake
        # if (self.controller.buttonR1.pressing()):
        #     self.intake.in_take()
        # elif(self.controller.buttonL1.pressing()):
        #     self.intake.out_take()
        # else:
        #     self.intake.stop()

        # Intake Pneumatics
        # if(self.controller.buttonUp.pressing()):
        #     open_pneumatics()
        # if(self.controller.buttonDown.pressing()):
        #     close_pneumatics()

        # Lift
        # if(self.controller.buttonR2.pressing()):
        #     self.lift.up()
        # if(self.controller.buttonL2.pressing()):
        #     self.lift.down()
        # else:
        #     self.lift.stop()

        # Bottom Intake
        # if(self.controller.buttonX.pressing()):
        #     self.conveyor.up()
        # if(self.controller.buttonY.pressing()):
        #     self.conveyor.down()
        # else:
        #     self.conveyor.stop()

    def user_control(self):
        self.brain.screen.clear_screen()
        self.brain.screen.print("driver control")

        while True:
            self.drive_control()
            self.toggle_control()
            self.claw_control()
            self.swing_arm_control()
            # self.lift_control()
            # self.intake_control()
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
