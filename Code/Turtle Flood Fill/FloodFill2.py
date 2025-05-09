import time, random

cx, cy = 0, 0

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

#temp
topIR, bottomIR, leftIR, rightIR = 0, 0, 0, 0
def wall(d):
    return random.randint(0,1) == 1
#endtemp

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
                #smoveTile("up")
            #Down
            elif CheckWall(currentPos, "down") != 1 and spaces[currentPos[0]][currentPos[1]-1] == nextVal:
                currentPos[1] -= 1
                #moveTile("down")
            #Left
            elif CheckWall(currentPos, "left") != 1 and spaces[currentPos[0]-1][currentPos[1]] == nextVal:
                currentPos[0] -= 1
                #moveTile("left")
            #Right
            elif CheckWall(currentPos, "right") != 1 and spaces[currentPos[0]+1][currentPos[1]] == nextVal:
                currentPos[0] += 1
                #moveTile("right")
            else:
                break

            time.sleep(0.05)

        time.sleep(0.05)

MazeSolve()