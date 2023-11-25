#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
yMotor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
xMotor1 = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
xMotor2 = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)


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

#Motor Setup
# yMotor.spin(REVERSE)
xMotor1.spin(REVERSE)
xMotor2.spin(REVERSE)

velo = 50;
def MoveX(velocity):
    xMotor1.set_velocity(-velocity, PERCENT)
    xMotor2.set_velocity(-velocity, PERCENT)

MoveX(velo)
while True:
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print(xMotor1.current(CurrentUnits.AMP))
    if(xMotor1.current(CurrentUnits.AMP) > 1.25):
        velo *= -1
        MoveX(velo)
    time.sleep(0.05)


