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
slowVelo = 10
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

# xMotor.set_stopping(HOLD)
# yMotor1.set_stopping(HOLD)
# yMotor2.set_stopping(HOLD)
xMotor.set_stopping(BRAKE)
yMotor1.set_stopping(BRAKE)
yMotor2.set_stopping(BRAKE)

#endregion

#region Function Def
def print(text):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print(text)

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

def zeroMaze():
    global x0, y0
    homeDevice()
    goto(x0, y0)

    xMotor.set_position(0,DEGREES)
    yMotor1.set_position(0,DEGREES)
    yMotor2.set_position(0,DEGREES)
    global cx, cy
    cx, cy = 0, 0

def moveTile(d):
    global cx, cy

    if d == "up":
        #move up until bottom ir can see the empty wall slot again
        movey(velo)
        while True:
            if (yMotor1.position(DEGREES) > (cy+0.75)*squareYDeg):
                if not wall(bottomIR):
                    break
        cy += 1

    elif d == "down":
        #move down until top ir can see the empty wall slot again
        movey(-velo)
        while True:
            if (yMotor1.position(DEGREES) > (cy-0.75)*squareYDeg):
                if not wall(topIR):
                    break
        cy -= 1

    elif d == "left":
        #move left until right ir can see the empty wall slot again
        movex(-velo)
        while True:
            if (xMotor.position(DEGREES) < (cx-0.75)*squareXDeg):
                if not wall(rightIR):
                    break
        cx -= 1
        
    elif d == "right":
        #move right until left ir can see the empty wall slot again
        movex(velo)
        while True:
            if (xMotor.position(DEGREES) > (cx+0.75)*squareXDeg):
                if not wall(leftIR):
                    break
        cx += 1
    else:
        raise Exception("Attempted to move in an unknown direction. (" + d + ")")
    
    #stop moving
    movey(0)
    movex(0)

def wall(IR):
    return IR.object_distance(MM) < 40
#endregion

#region Pathfinding
HEIGHT, WIDTH = 6,6
SQUARE_SIZE = 40
spaces = [[-1 for _ in range(HEIGHT)] for _ in range(WIDTH)]
#-1 : Unknown
# 0 : Clear
# 1 : Wall
verticalWalls = [[-1 for _ in range(HEIGHT)] for _ in range(WIDTH+1)]
for x in range(len(verticalWalls)):
    for y in range(len(verticalWalls[x])):
        if x == 0 or x == WIDTH:
            verticalWalls[x][y] = 1

horizontalWalls = [[-1 for _ in range(HEIGHT+1)] for _ in range(WIDTH)]
for x in range(len(horizontalWalls)):
    for y in range(len(horizontalWalls[x])):
        if y == 0 or y == HEIGHT:
            horizontalWalls[x][y] = 1

GoalSquares = [[WIDTH-1, HEIGHT-1]]

def CheckWall(pos, d):
    global horizontalWalls, verticalWalls
    if d == "up":
        return horizontalWalls[pos[0]][pos[1]+1]
    elif d == "down":
        return horizontalWalls[pos[0]][pos[1]]
    elif d == "right":
        return verticalWalls[pos[0]+1][pos[1]]
    elif d == "left":
        return verticalWalls[pos[0]][pos[1]]
    else:
        raise Exception("Attempted to check an unknown direction. (" + d + ")")

def SetWall(pos, d, v):
    global horizontalWalls, verticalWalls
    if d == "up":
        horizontalWalls[pos[0]][pos[1]+1] = v
    elif d == "down":
        horizontalWalls[pos[0]][pos[1]] = v
    elif d == "right":
        verticalWalls[pos[0]+1][pos[1]] = v
    elif d == "left":
        verticalWalls[pos[0]][pos[1]] = v
    else:
        raise Exception("Attempted to check an unknown direction. (" + d + ")")

def FloodFill():
    global cx, cy
    global horizontalWalls, verticalWalls

    #Create an empty array to start FloodFilling. 
    #Create a queue and add goal elements
    spaces = [[-1 for _ in range(HEIGHT)] for _ in range(WIDTH)]
    q = []
    for pos in GoalSquares:
        spaces[pos[0]][pos[1]] = 0
        q.append(pos)

    #Start searching elements
    while len(q) != 0:
        pos = q.pop(0)
        value = spaces[pos[0]][pos[1]] + 1
        
        #Up
        if CheckWall(pos, "up") != 1 and spaces[pos[0]][pos[1]+1] == -1:
            spaces[pos[0]][pos[1]+1]  = value
            q.append([pos[0],pos[1]+1] )

        #Down
        if CheckWall(pos, "down") != 1 and spaces[pos[0]][pos[1]-1] == -1:
            spaces[pos[0]][pos[1]-1] = value
            q.append([pos[0],pos[1]-1])

        #Left
        if CheckWall(pos, "left") != 1 and spaces[pos[0]-1][pos[1]] == -1:
            spaces[pos[0]-1][pos[1]] = value
            q.append([pos[0]-1,pos[1]])
        
        #Right
        if CheckWall(pos, "right") != 1 and spaces[pos[0]+1][pos[1]] == -1:
            spaces[pos[0]+1][pos[1]] = value
            q.append([pos[0]+1,pos[1]])
    return spaces

def UpdateWalls(pos):
    #Up
    if CheckWall(pos, "up") == -1:
        if wall(topIR):
            SetWall(pos, "up", 1)
        else:
            SetWall(pos, "up", 0)

    #Down
    if CheckWall(pos, "down") == -1:
        if wall(bottomIR):
            SetWall(pos, "down", 1)
        else:
            SetWall(pos, "down", 0)

    #Left
    if CheckWall(pos, "left") == -1:
        if wall(leftIR):
            SetWall(pos, "left", 1)
        else:
            SetWall(pos, "left", 0)

    #Right
    if CheckWall(pos, "right") == -1:
        if wall(rightIR):
            SetWall(pos, "right", 1)
        else:
            SetWall(pos, "right", 0)

def MazeSolve():
    global cx, cy
    currentPos = [cx,cy]
    finished = False
    while not finished:
        spaces = FloodFill()
        
        #No path to current node
        if spaces[currentPos[0]][currentPos[1]] == -1:
            finished = True
            print("No Solution")
            continue
        #Reached the end
        if spaces[currentPos[0]][currentPos[1]] == 0:
            finished = True
            print("Reached End")
            continue

        while True:
            UpdateWalls(currentPos)
            nextVal = spaces[currentPos[0]][currentPos[1]] - 1
            #Find Next Position
            #Up
            if CheckWall(currentPos, "up") != 1 and spaces[currentPos[0]][currentPos[1]+1] == nextVal:
                currentPos[1] += 1
                moveTile("up")
            #Down
            elif CheckWall(currentPos, "down") != 1 and spaces[currentPos[0]][currentPos[1]-1] == nextVal:
                currentPos[1] -= 1
                moveTile("down")
            #Left
            elif CheckWall(currentPos, "left") != 1 and spaces[currentPos[0]-1][currentPos[1]] == nextVal:
                currentPos[0] -= 1
                moveTile("left")
            #Right
            elif CheckWall(currentPos, "right") != 1 and spaces[currentPos[0]+1][currentPos[1]] == nextVal:
                currentPos[0] += 1
                moveTile("right")
            else:
                break

            time.sleep(0.05)

        time.sleep(0.05)
#endregion

#Actual Code
zeroMaze()
while not Button1.pressing():
    time.sleep(updateDelay)
MazeSolve()
