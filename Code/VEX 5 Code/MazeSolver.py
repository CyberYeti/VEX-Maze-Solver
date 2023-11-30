#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
yMotor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
xMotor1 = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
xMotor2 = Motor(Ports.PORT21, GearSetting.RATIO_18_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      Vex Maze Solver
#	Author:       Yit-Meng Chin
# 
# ------------------------------------------

# Library imports
import time

#Variables
waitDelay = 0.5
updateDelay = 0.05

#Degrees to mm
chainLinkLen = 25.5/25
dtmx = 12*chainLinkLen/360
dtmy = 6*chainLinkLen/360
maxdtm = max(abs(dtmx), abs(dtmy))

#Velocity Multipliers
#This is for making the speed of the x and y axis the same despite different gear ratios
vmx = abs(dtmy/maxdtm)
vmy = abs(dtmx/maxdtm)

#Motor Setup
yMotor.spin(FORWARD)
xMotor1.spin(FORWARD)
xMotor2.spin(FORWARD)

yMotor.set_velocity(0, PERCENT)
xMotor1.set_velocity(0, PERCENT)
xMotor2.set_velocity(0, PERCENT)

velo = 75
def movex(velocity):
    xMotor1.set_velocity(velocity*vmx, PERCENT)
    xMotor2.set_velocity(velocity*vmx, PERCENT)

def movey(velocity):
    yMotor.set_velocity(velocity*vmy, PERCENT)


def getx():
    return xMotor1.position(DEGREES)*dtmx

def gety():
    return yMotor.position(DEGREES)*dtmy

def collideX():
    return xMotor1.torque(TorqueUnits.INLB) > 5

def collideY():
    return yMotor.torque(TorqueUnits.INLB) > 2

# # Homing Sequence
# movex(-velo)
# time.sleep(waitDelay)
# while abs(xMotor1.velocity(PERCENT)) >= 1:
#     time.sleep(updateDelay)
# movex(0)
# xMotor1.set_position(0,DEGREES)
# xMotor2.set_position(0,DEGREES)

# movey(-velo)
# time.sleep(waitDelay)
# while abs(yMotor.velocity(PERCENT)) >= 1:
#     time.sleep(updateDelay)
# movey(0)
# yMotor.set_position(0,DEGREES)

# #Find Torque Thresholds
# movex(velo)
# time.sleep(waitDelay)
# maxTorque = 0
# while abs(xMotor1.velocity(PERCENT)) >= 1:
#     maxTorque = max(xMotor1.torque(TorqueUnits.INLB), maxTorque)
#     brain.screen.clear_screen()
#     brain.screen.set_cursor(1, 1)
#     brain.screen.print("x:", maxTorque)
#     time.sleep(updateDelay)
# movex(0)

# time.sleep(10)

# movey(velo)
# time.sleep(waitDelay)
# maxTorque = 0
# while abs(yMotor.velocity(PERCENT)) >= 1:
#     maxTorque = max(yMotor.torque(TorqueUnits.INLB), maxTorque)
#     brain.screen.clear_screen()
#     brain.screen.set_cursor(1, 1)
#     brain.screen.print("y:", maxTorque)
#     time.sleep(updateDelay)
# movey(0)


# Homing Sequence using torque
movex(-velo)
time.sleep(waitDelay)
while not collideX():
    time.sleep(updateDelay)
movex(0)
xMotor1.set_position(0,DEGREES)
xMotor2.set_position(0,DEGREES)

movey(-velo)
time.sleep(waitDelay)
while not collideY():
    time.sleep(updateDelay)
movey(0)
yMotor.set_position(0,DEGREES)