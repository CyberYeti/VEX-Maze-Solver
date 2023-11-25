import random, queue
def DFSMaze(l, w):
    mapVW = [[1 for _ in range(l+1)] for _ in range(w)]
    mapHW = [[1 for _ in range(l)] for _ in range(w+1)]
    # start = [random.randint(0,w-1),random.randint(0,l-1)]
    # end = [random.randint(0,w-1),random.randint(0,l-1)]
    # while start == end:
    #     end = [random.randint(0,w-1),random.randint(0,l-1)]
    start = [0,0]
    end = [l-1,w-1]

    #0 Not Searched
    #1 Searched
    grid = [[0 for _ in range(l)] for _ in range(w)]
    cp = end.copy()
    q = queue.LifoQueue()
    q.put(cp.copy())
    grid[cp[0]][cp[1]] = 1
    while not q.empty():
        #Check Surrounding Directions
        #0:up
        # 1:right
        # 2:down
        # 3:left
        dir = []
        if cp[0] > 0 and grid[cp[0]-1][cp[1]] == 0:
            dir.append(0)
        if cp[0] < w-1 and grid[cp[0]+1][cp[1]] == 0:
            dir.append(2)
        if cp[1] > 0 and grid[cp[0]][cp[1]-1] == 0:
            dir.append(3)
        if cp[1] < l-1 and grid[cp[0]][cp[1]+1] == 0:
            dir.append(1)
        
        if len(dir) == 0:
            cp = q.get().copy()
        else:
            d = random.choice(dir)
            if d == 0:
                mapHW[cp[0]][cp[1]] = 0
                cp[0]-=1
            if d == 1:
                mapVW[cp[0]][cp[1]+1] = 0
                cp[1]+=1
            if d == 2:
                mapHW[cp[0]+1][cp[1]] = 0
                cp[0]+=1
            if d == 3:
                mapVW[cp[0]][cp[1]] = 0
                cp[1]-=1
            q.put(cp.copy())
            grid[cp[0]][cp[1]] = 1


    return mapVW, mapHW, start, end

def BasicMaze(l, w):
    mapVW = [[1,*[random.randint(0,1) for i in range(l-1)], 1] for i in range(w)]
    mapHW = [[1 for i in range(l)], *[[random.randint(0,1) for i in range(l)] for i in range(w-1)], [1 for i in range(l)]]
    start = [random.randint(0,w-1),random.randint(0,l-1)]
    end = [random.randint(0,w-1),random.randint(0,l-1)]
    while start == end:
        end = [random.randint(0,w-1),random.randint(0,l-1)]

    return mapVW, mapHW, start, end

