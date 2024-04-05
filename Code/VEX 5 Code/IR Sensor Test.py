#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
bottomIR = Distance(Ports.PORT1)
leftIR = Distance(Ports.PORT2)
rightIR = Distance(Ports.PORT16)
topIR = Distance(Ports.PORT17)


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
# 	Project:      Ir Sensor Test
#	Author:       Yit-Meng
# 
# ------------------------------------------

'''
Sensor Ports
topIR = 17
bottomIR = 1
leftIR = 2
rightIR = 16
'''

# Library imports
from vex import *
import time

# Begin project code
def wall(IR):
    return IR.object_distance(MM) < 20

while True:
    time.sleep(0.05)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Top has wall:" + str(wall(topIR)))
    brain.screen.set_cursor(2,1)
    brain.screen.print("Bottom has wall:" + str(wall(bottomIR)))
    brain.screen.set_cursor(3,1)
    brain.screen.print("Left has wall:" + str(wall(leftIR)))
    brain.screen.set_cursor(4,1)
    brain.screen.print("Right has wall:" + str(wall(rightIR)))