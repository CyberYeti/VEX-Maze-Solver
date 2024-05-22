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
AdjustUP = Bumper(brain.three_wire_port.f)
AdjustDown = Bumper(brain.three_wire_port.h)
xMotor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
yMotor1 = Motor(Ports.PORT21, GearSetting.RATIO_18_1, False)
yMotor2 = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
Button1 = Bumper(brain.three_wire_port.a)


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
velo = 12.5
waitDelay = 0.5
updateDelay = 0.05
tolerence = 1

#Maze Info
ROW, COL = 6, 6
squareXDeg = 1067/5 #degrees x motor needs to turn to move 1 square
squareYDeg = 525/5 #degrees y motor needs to turn to move 1 square
x0, y0 = 174, 114 #represents the position of the first grid square
cx, cx = 0, 0 #represents the current coordinate

xTorqueThesh = 3
yTorqueThesh = 6

#Velocity Multipliers
#This is for making the speed of the x and y axis the same despite different gear ratios
xTeeth = 6
yTeeth = 12
maxTeeth = max(xTeeth, yTeeth)
vmx = xTeeth/maxTeeth
vmy = yTeeth/maxTeeth

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
    return yMotor1.position(DEGREES)

def getx():
    return xMotor.position(DEGREES)

def collideY():
    return yMotor1.torque(TorqueUnits.INLB) > yTorqueThesh

def collideX():
    return xMotor.torque(TorqueUnits.INLB) > xTorqueThesh

def homeDevice():
    # Homing Sequence
    # Home Y
    # First Home
    movey(-75)
    time.sleep(waitDelay)
    while not collideY():
        time.sleep(updateDelay)
    movey(0)
    yMotor1.set_position(0,DEGREES)
    yMotor2.set_position(0,DEGREES)
    time.sleep(0.05)

    # Move Back again for second Home
    movey(75)
    while yMotor1.position(DEGREES) < 90:
        pass

    #Second Home
    movey(-10)
    time.sleep(waitDelay)
    while not collideY():
        time.sleep(updateDelay)
    movey(0)
    yMotor1.set_position(0,DEGREES)
    yMotor2.set_position(0,DEGREES)



    # Home X
    movex(-75)
    time.sleep(waitDelay)
    while not collideX():
        time.sleep(updateDelay)
    movex(0)
    xMotor.set_position(0,DEGREES)

    # Move Back again for second Home
    movex(75)
    while xMotor.position(DEGREES) < 90:
        pass

    # Second Home
    movex(-10)
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

def moveToTile(x,y):
    #keeps the targeted tile in bounds
    global cx, cy
    cx = min(max(x,0),5)
    cy = min(max(y,0),5)

    #send error if out of bounds
    if cx != x or cy != y:
        raise Exception("Attempted to move to a tile out of bounds. (" + str(x) + "," + str(y) + ")")

    tx = cx*squareXDeg
    ty = cy*squareYDeg
    goto(tx, ty)

    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("(" + str(tx-xMotor.position(DEGREES)) + "," + str(ty-yMotor1.position(DEGREES)) + ")")

    time.sleep(1)

def moveTile(d):
    global cx, cy

    if d == "up":
        #make sure target direction does not have a wall
        if wall(topIR):
            raise Exception("Attempted to move in a blocked direction. (" + d + ")")

        #move up until bottom ir can see the empty wall slot again
        movey(velo)
        while True:
            if (yMotor1.position(DEGREES) > (cy+0.5)*squareYDeg) and not wall(bottomIR):
                break
            time.sleep(updateDelay)
        cy += 1

    elif d == "down":
        #make sure target direction does not have a wall
        if wall(bottomIR):
            raise Exception("Attempted to move in a blocked direction. (" + d + ")")

        #move down until top ir can see the empty wall slot again
        movey(-velo)
        while True:
            if (yMotor1.position(DEGREES) < (cy-0.5)*squareYDeg) and not wall(topIR):
                break
            time.sleep(updateDelay)
        cy -= 1

    elif d == "left":
        #make sure target direction does not have a wall
        if wall(leftIR):
            raise Exception("Attempted to move in a blocked direction. (" + d + ")")
            
        #move left until right ir can see the empty wall slot again
        movex(-velo)
        while True:
            if (xMotor.position(DEGREES) < (cx-0.5)*squareXDeg) and not wall(rightIR):
                break
            time.sleep(updateDelay)
        cx -= 1
        
    elif d == "right":
        #make sure target direction does not have a wall
        if wall(rightIR):
            raise Exception("Attempted to move in a blocked direction. (" + d + ")")
            
        #move right until left ir can see the empty wall slot again
        movex(velo)
        while True:
            if (xMotor.position(DEGREES) > (cx+0.5)*squareXDeg) and not wall(leftIR):
                break
            time.sleep(updateDelay)
        cx += 1
    else:
        raise Exception("Attempted to move in an unknown direction. (" + d + ")")
    
    #stop moving
    movey(0)
    movex(0)

def zeroMaze():
    global x0, y0
    homeDevice()
    goto(x0, y0)

    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Adjust X")
    while not Button1.pressing():
        if AdjustUP.pressing():
            x0 += 5;
            goto(x0, y0)
        elif AdjustDown.pressing():
            x0 -= 5;
            goto(x0, y0)

    while Button1.pressing():
        time.sleep(updateDelay)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Adjust Y")
    while not Button1.pressing():
        if AdjustUP.pressing():
            y0 += 5;
            goto(x0, y0)
        elif AdjustDown.pressing():
            y0 -= 5;
            goto(x0, y0)

    xMotor.set_position(0,DEGREES)
    yMotor1.set_position(0,DEGREES)
    yMotor2.set_position(0,DEGREES)
    global cx, cy
    cx, cy = 0, 0

def wall(IR):
    return IR.object_distance(MM) < 20
#endregion

#Actual Code
while True:
    zeroMaze()
    
    px, py = -1, -1
    pdir = ""
    while True:
        if not wall(topIR) and pdir != "d":
            moveTile("up")
            pdir = "u"
        elif not wall(bottomIR) and pdir != "u":
            moveTile("down")
            pdir = "d"
        elif not wall(leftIR) and pdir != "r":
            moveTile("left")
            pdir = "l"
        elif not wall(rightIR) and pdir != "l":
            moveTile("right")
            pdir = "r"
        else:
            break

        px = cx
        py = cy

        # brain.screen.clear_screen()
        # brain.screen.set_cursor(1,1)
        # brain.screen.print("(" + str(cx) + "," + str(cy) + ")")
        time.sleep(0.05)

    # brain.screen.clear_screen()
    # brain.screen.set_cursor(1,1)
    # brain.screen.print("Exited At (" + str(cx) + "," + str(cy) + ")")
    
    while not Button1.pressing():
        time.sleep(updateDelay)