# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       ibrahimhelal, Jackson, Reid, Bruno                           #
# 	Created:      4/23/2026, 6:07:40 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import * # `type: ignore

class Intake:
    def __init__(self, half_motor):
        self.half_motor = half_motor

    def in_take(self):
        # Code to intake
        self.half_motor.spin(FORWARD, 100, PERCENT)

    def out_take(self):
        # Code to intake
        self.half_motor.spin(REVERSE, 100, PERCENT)

    def release(self):
        # Code to intake
        self.half_motor.stop()

class Conveyer:
    def __init__(self, conveyer_motor):
        self.conveyer_motor = conveyer_motor

    def intake(self):
        self.conveyer_motor.spin(FORWARD, 100, PERCENT)

    def outtake(self):
        self.conveyer_motor.spin(REVERSE, 100, PERCENT)

    def release(self):
        self.conveyer_motor.stop

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
        self._pneumatics.set(True)

    def close(self):
        self._pneumatics.set(False)

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
        fl = Motor(Ports.PORT12, True)
        fr = Motor(Ports.PORT11, False)
        bl = Motor(Ports.PORT4, True)
        br = Motor(Ports.PORT8, False)
        self.drive_base = MecanumDrive(fl, fr, bl, br)

        intake_motor = Motor(Ports.PORT5, False)
        self.intake = Intake(intake_motor)
        self.conveyer_motor = Conveyer(Motor(Ports.PORT6, False))
        self.claw = Claw(Motor(Ports.PORT2, True))
        self.swing_arm = Swingarm(Motor(Ports.PORT10))
        self.lift = Lift(Motor(Ports.PORT20))
        self.toggle = Toggle(Motor(Ports.PORT9))
        self.pneumatics = Pneumatics(DigitalOut(self.brain.three_wire_port.a))

    def autonomous(self):
        self.brain.screen.clear_screen()
        self.brain.screen.print("autonomous code")
        # self.inertial.calibrate()
        # wait(2, SECONDS)
        self.toggle.turn_down
        
        self.toggle.stop
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
        if (self.controller.buttonL1.pressing()):
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
        self.brain.screen.print("FL: " + str(self.drive_base.fl.temperature(TemperatureUnits.FAHRENHEIT)) + "°F | FR: " + str(self.drive_base.fr.temperature(TemperatureUnits.FAHRENHEIT)) + "°F")
        self.brain.screen.set_cursor(3, 1)
        self.brain.screen.print("BL: " + str(self.drive_base.bl.temperature(TemperatureUnits.FAHRENHEIT)) + "°F | BR: " + str(self.drive_base.br.temperature(TemperatureUnits.FAHRENHEIT)) + "°F")
        self.brain.screen.set_cursor(6, 1)
        self.brain.screen.print("Motors work well below 120°F")
        self.brain.screen.set_cursor(4, 1)
        self.brain.screen.print("bottom intake: " + str(self.conveyer_motor.conveyer_motor.temperature(TemperatureUnits.FAHRENHEIT)) + "°F") 
        self.brain.screen.set_cursor(5, 1)
        self.brain.screen.print("top intake: " + str(self.intake.half_motor.temperature(TemperatureUnits.FAHRENHEIT)) + "°F")

    def lift_control(self):
            # Lift
        if(self.controller.buttonR2.pressing()):
            self.lift.up()
        elif(self.controller.buttonL2.pressing()):
            self.lift.down()
        else:
            self.lift.stop()

    def intake_control(self):
        # Intake
        if (self.controller.buttonR1.pressing()):
            self.intake.in_take()
        elif (self.controller.buttonR2.pressing()):
                    self.intake.out_take()
        elif (self.controller.buttonUp.pressing):
            self.intake.release

        # Intake Pneumatics
    
        if(self.controller.buttonUp.pressing()):
             self.pneumatics.open()
        if(self.controller.buttonDown.pressing()):
             self.pneumatics.close()

        # Lift
        if(self.controller.buttonR2.pressing()):
            self.lift.up()
        elif(self.controller.buttonL2.pressing()):
            self.lift.down()
        else:
            self.lift.stop()
            
        # Bottom Intake
        if(self.controller.buttonR1.pressing()):
            self.conveyer_motor.outtake()
        elif(self.controller.buttonR2.pressing()):
            self.conveyer_motor.intake()
       

    def user_control(self):
        self.brain.screen.clear_screen()
        self.brain.screen.print("driver control")

        while True:
            self.drive_control()
            self.toggle_control()
            self.claw_control()
            self.swing_arm_control()
            self.lift_control()
            self.intake_control()
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
