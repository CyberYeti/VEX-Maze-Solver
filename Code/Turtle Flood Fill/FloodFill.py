import queue
from turtle import Screen, Turtle
import time
import MazeGen
#region parameters
LENGTH, WIDTH = 6,6
SQUARE_SIZE = 40
spaces = [[-1 for i in range(LENGTH)] for i in range(WIDTH)]
#-1 : Unknown
# 0 : Clear
# 1 : Wall
verticalWalls = [[1, *[-1 for i in range(LENGTH-1)], 1] for i in range(WIDTH)]
horizontalWalls = [[1 for i in range(LENGTH)], *[[-1 for i in range(LENGTH)] for i in range(WIDTH-1)], [1 for i in range(LENGTH)]]
#coordinates are in a (y,x) format
#Randomly Generate Maze
GoalSquares = [[]]
mapVW, mapHW, startPosition, GoalSquares[0] = MazeGen.DFSMaze(LENGTH, WIDTH)
mapVW = [
    [1,0,1,0,0,0,1],
    [1,0,0,1,1,1,1],
    [1,1,0,0,1,1,1],
    [1,1,0,1,1,0,1],
    [1,1,1,0,1,0,1],
    [1,0,1,0,1,0,1]
]
mapHW = [
    [1,1,1,1,1,1],
    [0,1,0,1,0,0],
    [0,1,1,0,0,0],
    [0,1,0,0,0,1],
    [0,0,1,0,1,0],
    [0,0,0,1,0,1],
    [1,1,1,1,1,1]
]

#endregion
#region Functions
def FloodFill(vWalls, hWalls):
    #Create an empty array to start FloodFilling. 
    #Create a queue and add goal elements
    spaces = [[-1 for i in range(LENGTH)] for i in range(WIDTH)]
    q = queue.Queue()
    for pos in GoalSquares:
        spaces[pos[0]][pos[1]] = 0
        q.put(pos)
    #Start searching elements
    while not q.empty():
        pos =  q.get()
        value = spaces[pos[0]][pos[1]] + 1
        
        #Up
        if horizontalWalls[pos[0]][pos[1]] != 1 and spaces[pos[0]-1][pos[1]] == -1:
            spaces[pos[0]-1][pos[1]] = value
            q.put([pos[0]-1,pos[1]])
        #Down
        if horizontalWalls[pos[0]+1][pos[1]] != 1 and spaces[pos[0]+1][pos[1]] == -1:
            spaces[pos[0]+1][pos[1]] = value
            q.put([pos[0]+1, pos[1]])
        #Left
        if verticalWalls[pos[0]][pos[1]] != 1 and spaces[pos[0]][pos[1]-1] == -1:
            spaces[pos[0]][pos[1]-1] = value
            q.put([pos[0], pos[1]-1])
        
        #Right
        if verticalWalls[pos[0]][pos[1]+1] != 1 and spaces[pos[0]][pos[1]+1] == -1:
            spaces[pos[0]][pos[1]+1] = value
            q.put([pos[0], pos[1]+1])
    return spaces
def CheckWalls(pos):
    #Up
    if horizontalWalls[pos[0]][pos[1]] == -1:
        horizontalWalls[pos[0]][pos[1]] = mapHW[pos[0]][pos[1]]
        if horizontalWalls[pos[0]][pos[1]] == 1:
            DrawHorizontalWall(pos[0], pos[1], "Black")
    #Down
    if horizontalWalls[pos[0]+1][pos[1]] == -1:
        horizontalWalls[pos[0]+1][pos[1]] = mapHW[pos[0]+1][pos[1]]
        if horizontalWalls[pos[0]+1][pos[1]] == 1:
            DrawHorizontalWall(pos[0]+1, pos[1], "Black")
    #Left
    if verticalWalls[pos[0]][pos[1]] == -1:
        verticalWalls[pos[0]][pos[1]] = mapVW[pos[0]][pos[1]]
        if verticalWalls[pos[0]][pos[1]] == 1:
            DrawVerticalWall(pos[0], pos[1], "Black")
    
    #Right
    if verticalWalls[pos[0]][pos[1]+1] == -1:
        verticalWalls[pos[0]][pos[1]+1] = mapVW[pos[0]][pos[1]+1]
        if verticalWalls[pos[0]][pos[1]+1] == 1:
            DrawVerticalWall(pos[0], pos[1]+1, "Black")
def DrawVerticalWall(y, x, color):
    pen.pencolor(color)
    pen.width(5)
    pen.setheading(90)
    pen.penup()
    pen.goto(x*SQUARE_SIZE, y*SQUARE_SIZE)
    pen.pendown()
    pen.forward(SQUARE_SIZE)
def DrawHorizontalWall(y, x, color):
    pen.pencolor(color)
    pen.width(5)
    pen.setheading(0)
    pen.penup()
    pen.goto(x*SQUARE_SIZE, y*SQUARE_SIZE)
    pen.pendown()
    pen.forward(SQUARE_SIZE)
def DrawPath(color, position):
    currentPos = position
    pen.pencolor(color)
    pen.penup()
    pen.goto(currentPos[1]*SQUARE_SIZE + SQUARE_SIZE/2, currentPos[0]*SQUARE_SIZE + SQUARE_SIZE/2)
    pen.pendown()
    while spaces[currentPos[0]][currentPos[1]] > 0:
        nextVal = spaces[currentPos[0]][currentPos[1]] - 1
        #Up
        if horizontalWalls[currentPos[0]][currentPos[1]] != 1 and spaces[currentPos[0]-1][currentPos[1]] == nextVal:
            currentPos[0] -= 1
        #Down
        elif horizontalWalls[currentPos[0]+1][currentPos[1]] != 1 and spaces[currentPos[0]+1][currentPos[1]] == nextVal:
            currentPos[0] += 1
        #Left
        elif verticalWalls[currentPos[0]][currentPos[1]] != 1 and spaces[currentPos[0]][currentPos[1]-1] == nextVal:
            currentPos[1] -= 1
        #Right
        elif verticalWalls[currentPos[0]][currentPos[1]+1] != 1 and spaces[currentPos[0]][currentPos[1]+1] == nextVal:
            currentPos[1] += 1
        else:
            break
        
        pen.goto(currentPos[1]*SQUARE_SIZE + SQUARE_SIZE/2, currentPos[0]*SQUARE_SIZE + SQUARE_SIZE/2)
#endregion
#region Graphics Setup
screen = Screen()
screen.setup(LENGTH*SQUARE_SIZE + 5, WIDTH*SQUARE_SIZE + 5)
screen.setworldcoordinates(0, 0, LENGTH*SQUARE_SIZE, WIDTH*SQUARE_SIZE)
screen.setup(1.0, 1.0)
screen.title("Maze")
pen = Turtle()
pen.speed(0)
pen.hideturtle()
pen.pencolor("Black")
pen.penup()
pen.goto(0,0)
pen.pendown()
#Draw Frame
for i in range(2):
    pen.forward(LENGTH*SQUARE_SIZE)
    pen.left(90)
    pen.forward(WIDTH*SQUARE_SIZE)
    pen.left(90)
#Draw Grid
pen.setheading(90)
pen.pencolor("Grey")
for i in range(LENGTH-1):
    pen.penup()
    pen.goto((i+1)*SQUARE_SIZE, 0)
    pen.pendown()
    pen.forward(WIDTH*SQUARE_SIZE)
pen.setheading(0)
for i in range(WIDTH-1):
    pen.penup()
    pen.goto(0, (i+1)*SQUARE_SIZE)
    pen.pendown()
    pen.forward(LENGTH*SQUARE_SIZE)
#Fill Start and end
pen.fillcolor("Lime")
pen.penup()
pen.setheading(0)
for pos in GoalSquares:
    pen.goto(pos[1]*SQUARE_SIZE+1, pos[0]*SQUARE_SIZE)
    pen.begin_fill()
    for i in range(4):
        pen.forward(SQUARE_SIZE-1)
        pen.left(90)
    pen.end_fill()
pen.fillcolor("Red")
pen.goto(startPosition[1]*SQUARE_SIZE+1, startPosition[0]*SQUARE_SIZE)
pen.begin_fill()
for i in range(4):
    pen.forward(SQUARE_SIZE-1)
    pen.left(90)
pen.end_fill()
#Draw Map Walls
# pen.pencolor("Blue")
# pen.width(5)
# for x in range(LENGTH+1):
#     s = [0,x]
#     for y in range(WIDTH):
#         if mapVW[y][x] != 1:
#             if s != [y,x]:
#                 pen.penup()
#                 pen.goto(s[1]*SQUARE_SIZE, s[0]*SQUARE_SIZE)
#                 pen.pendown()
#                 pen.goto(x*SQUARE_SIZE, y*SQUARE_SIZE)
#             s = [y+1,x]
#     if s != [WIDTH,x]:
#         pen.penup()
#         pen.goto(s[1]*SQUARE_SIZE, s[0]*SQUARE_SIZE)
#         pen.pendown()
#         pen.goto(x*SQUARE_SIZE, WIDTH*SQUARE_SIZE)
# pen.penup()
# for y in range(WIDTH+1):
#     s = [y,0]
#     for x in range(LENGTH):
#         if mapHW[y][x] != 1:
#             if s != [y,x]:
#                 pen.penup()
#                 pen.goto(s[1]*SQUARE_SIZE, s[0]*SQUARE_SIZE)
#                 pen.pendown()
#                 pen.goto(x*SQUARE_SIZE, y*SQUARE_SIZE)
#             s = [y,x+1]
#     if s != [y,LENGTH]:
#         pen.penup()
#         pen.goto(s[1]*SQUARE_SIZE, s[0]*SQUARE_SIZE)
#         pen.pendown()
#         pen.goto(LENGTH*SQUARE_SIZE, y*SQUARE_SIZE)
#Draw Known Walls
pen.pencolor("Black")
pen.width(5)
pen.penup()
pen.goto(0,0)
pen.pendown()
pen.setheading(0)
for i in range(2):
    pen.forward(LENGTH*SQUARE_SIZE)
    pen.left(90)
    pen.forward(WIDTH*SQUARE_SIZE)
    pen.left(90)
#endregion
t = Turtle()
t.hideturtle()
t.speed(1)
t.shape("circle")
t.color("Black")
t.penup()
t.goto(startPosition[1]*SQUARE_SIZE + SQUARE_SIZE/2, startPosition[0]*SQUARE_SIZE + SQUARE_SIZE/2)
t.showturtle()
currentPos = startPosition.copy()
finished = False
while not finished:
    spaces = FloodFill(verticalWalls, horizontalWalls)
    
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
        CheckWalls(currentPos)
        nextVal = spaces[currentPos[0]][currentPos[1]] - 1
        #Find Next Position
        #Up
        if horizontalWalls[currentPos[0]][currentPos[1]] != 1 and spaces[currentPos[0]-1][currentPos[1]] == nextVal:
            currentPos[0] -= 1
        #Down
        elif horizontalWalls[currentPos[0]+1][currentPos[1]] != 1 and spaces[currentPos[0]+1][currentPos[1]] == nextVal:
            currentPos[0] += 1
        #Left
        elif verticalWalls[currentPos[0]][currentPos[1]] != 1 and spaces[currentPos[0]][currentPos[1]-1] == nextVal:
            currentPos[1] -= 1
        #Right
        elif verticalWalls[currentPos[0]][currentPos[1]+1] != 1 and spaces[currentPos[0]][currentPos[1]+1] == nextVal:
            currentPos[1] += 1
        else:
            break
        
        t.goto(currentPos[1]*SQUARE_SIZE + SQUARE_SIZE/2, currentPos[0]*SQUARE_SIZE + SQUARE_SIZE/2)
        time.sleep(0.05)
    time.sleep(0.05)
    screen.update()
DrawPath("Orange", startPosition.copy())
while True:
    screen.update()