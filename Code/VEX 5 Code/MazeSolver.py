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

velo = 75;
def movex(velocity):
    xMotor1.set_velocity(velocity*vmx, PERCENT)
    xMotor2.set_velocity(velocity*vmx, PERCENT)

def movey(velocity):
    yMotor.set_velocity(velocity*vmy, PERCENT)


def getx():
    return xMotor1.position(DEGREES)*dtmx

def gety():
    return yMotor.position(DEGREES)*dtmy

# Homing Sequence
movex(-velo)
time.sleep(waitDelay)
while xMotor1.current(CurrentUnits.AMP) < 2:
    time.sleep(updateDelay)
movex(0)
xMotor1.set_position(0,DEGREES)
xMotor2.set_position(0,DEGREES)

movey(-velo)
time.sleep(waitDelay)
while yMotor.current(CurrentUnits.AMP) < 1:
    time.sleep(updateDelay)
movey(0)
yMotor.set_position(0,DEGREES)

#Find Bounds
movex(velo)
time.sleep(waitDelay)
while xMotor1.current(CurrentUnits.AMP) < 2:
    pass
movex(0)

movey(velo)
time.sleep(waitDelay)
while yMotor.current(CurrentUnits.AMP) < 1:
    pass
movey(0)

brain.screen.print("x:", getx(), "   y:", gety())

#Random Movement
movex(-velo)
time.sleep(waitDelay)
while xMotor1.current(CurrentUnits.AMP) < 2:
    time.sleep(updateDelay)
movex(0)
xMotor1.set_position(0,DEGREES)
xMotor2.set_position(0,DEGREES)

movey(-velo)
time.sleep(waitDelay)
while yMotor.current(CurrentUnits.AMP) < 1:
    time.sleep(updateDelay)
movey(0)
yMotor.set_position(0,DEGREES)

movex(velo)
movey(velo)
time.sleep(waitDelay)
while (xMotor1.current(CurrentUnits.AMP) < 2) and (yMotor.current(CurrentUnits.AMP) < 1):
    time.sleep(updateDelay)
movex(0)
movey(0)

# # Collision Detection Test
# movex(velo)
# while True:
#     brain.screen.clear_screen()
#     brain.screen.set_cursor(1, 1)
#     brain.screen.print(xMotor1.current(CurrentUnits.AMP))
#     if(xMotor1.current(CurrentUnits.AMP) > 1.25):
#         velo *= -1
#         movex(velo)
#     time.sleep(0.05)