#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code


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
import time, math

#region Variables
velo = 75
waitDelay = 0.5
updateDelay = 0.05
tolerence = 2

#Maze Info
ROW, COL = 6, 6
SQUARE_SIZE = 35
x0, y0 = 47.5, 30 #represents the position of the first grid square
cx, cx = 0, 0 #represents the current coordinate

xTorqueThesh = 2
yTorqueThesh = 5

#Degrees to mm
chainLinkLen = 255.0/25
dtmx = 12*chainLinkLen/360
dtmy = 6*chainLinkLen/360
maxdtm = max(abs(dtmx), abs(dtmy))

#Velocity Multipliers
#This is for making the speed of the x and y axis the same despite different gear ratios
vmx = abs(dtmy/maxdtm)
vmy = abs(dtmx/maxdtm)

#endregion

#region Motor Setup
xMotor.spin(FORWARD)
yMotor1.spin(FORWARD)
yMotor2.spin(FORWARD)

xMotor.set_velocity(0, PERCENT)
yMotor1.set_velocity(0, PERCENT)
yMotor2.set_velocity(0, PERCENT)

xMotor.set_stopping(HOLD)
yMotor1.set_stopping(HOLD)
yMotor2.set_stopping(HOLD)

#endregion

#region Function Def
def movey(velocity):
    if velocity == 0:
        yMotor1.stop()
        yMotor2.stop()
    else:
        yMotor1.spin(FORWARD)
        yMotor2.spin(FORWARD)
        yMotor1.set_velocity(velocity*vmx, PERCENT)
        yMotor2.set_velocity(velocity*vmx, PERCENT)

def movex(velocity):
    if velocity == 0:
        xMotor.stop()
    else:
        xMotor.spin(FORWARD)
        xMotor.set_velocity(velocity*vmy, PERCENT)

def gety():
    return yMotor1.position(DEGREES)*dtmx

def getx():
    return xMotor.position(DEGREES)*dtmy

def collideY():
    return yMotor1.torque(TorqueUnits.INLB) > yTorqueThesh

def collideX():
    return xMotor.torque(TorqueUnits.INLB) > xTorqueThesh

def homeDevice():
    # Homing Sequence
    movey(-velo)
    time.sleep(waitDelay)
    while not collideY():
        time.sleep(updateDelay)
    movey(0)
    yMotor1.set_position(0,DEGREES)
    yMotor2.set_position(0,DEGREES)

    movex(-velo)
    time.sleep(waitDelay)
    while not collideX():
        time.sleep(updateDelay)
    movex(0)
    xMotor.set_position(0,DEGREES)

def goto(x,y):
    dx = x - getx()
    dy = y - gety()
    while (abs(dx) > tolerence) or (abs(dy) > tolerence):
        dx = x - getx()
        dy = y - gety()
        if abs(dx) > tolerence:
            movex(math.copysign(velo, dx))
        else:
            movex(0)

        if abs(dy) > tolerence:
            movey(math.copysign(velo, dy))
        else:
            movey(0)

#A possible future version of goto that would detect whether it has collided with something
#while traveling and return to its inital position if so
def gotoCol(x,y):
    ix, iy = getx(), gety() #initial x and y
    tx, ty = x, y #Targeted x and y
    collided = False

    dx = tx - ix
    dy = ty - iy

    brain.timer.clear()
    while (abs(dx) > tolerence) or (abs(dy) > tolerence):
        dx = tx - getx()
        dy = ty - gety()
        if abs(dx) > tolerence:
            movex(math.copysign(velo, dx))
        else:
            movex(0)

        if abs(dy) > tolerence:
            movey(math.copysign(velo, dy))
        else:
            movey(0)

        if abs(dx) > 10 and abs(dy) > 10 and brain.timer.time(SECONDS) > waitDelay and (collideY() or collideX()):
            brain.screen.clear_screen()
            brain.screen.set_cursor(1,1)
            brain.screen.print("x:", collideX())
            brain.screen.set_cursor(2,1)
            brain.screen.print("y:", collideY())
            collided = True
            tx, ty = ix, iy

        time.sleep(updateDelay)
    
    return collided

def zeroMaze():
    homeDevice()
    goto(x0, y0)
    xMotor.set_position(0,DEGREES)
    yMotor1.set_position(0,DEGREES)
    yMotor2.set_position(0,DEGREES)
    global cx, cy
    cx, cy = 0, 0

#These two movement functions are created to prevent me from accidentally making diagonal moves.
def moveVerticalTile(numTiles):
    global cy
    cy = cy + numTiles
    cy = min(cy, ROW-1)
    cy = max(cy, 0)
        
    goto(cx*(SQUARE_SIZE + 2), cy*(SQUARE_SIZE + 1))

def moveHorizontalTile(numTiles):
    global cx
    cx = cx + numTiles
    cx = min(cx, COL-1)
    cx = max(cx, 0)
        
    goto(cx*(SQUARE_SIZE + 2), cy*(SQUARE_SIZE + 1))
#endregion

# homeDevice()
zeroMaze()
time.sleep(waitDelay)
moveVerticalTile(5)
moveHorizontalTile(5)
moveVerticalTile(-5)


time.sleep(waitDelay)
gotoCol(0,0)