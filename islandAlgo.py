#This is a script to help create a random island


import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from os import system as cmd
from datetime import datetime


testPoints = []
testPoints2 = []
def AddRandomPointsToGrid(grid, numPoints, gauss=False, mean=0, std=0):
    for i in range(0,numPoints):
        if gauss == False:
            x = random.randint(0,len(grid)-1)
            y = random.randint(0,len(grid[0])-1)
        else:
            while True:
                nn = 40
                x = DiscreteGaussianDraw(mean,std)+int(len(grid)/2)
                y = DiscreteGaussianDraw(mean,std)+int(len(grid[0])/2)
                if x >= nn and y >= nn and x <= len(grid)-nn and y <= len(grid[0])-nn:
                    break
        try:
            grid[x][y] = 1
        except IndexError:
            pass
    return grid

def ChangeIsolatedPoints(grid):
    for i in range(0,len(grid)):
        for j in range(0,len(grid[0])):
            if grid[i][j] == 1:
                cnt = 0
                ect = 0
                try:
                    if grid[i+1][j] == 0: 
                        cnt += 1
                except IndexError:
                    ect += 1
                try:
                    if grid[i-1][j] == 0:
                        cnt += 1
                except IndexError:
                    ect += 1
                try:
                    if grid[i][j+1] == 0:
                        cnt += 1
                except IndexError:
                    ect += 1
                try:
                    if grid[i][j-1] == 0:
                        cnt += 1
                except IndexError:
                    ect += 1                
                if cnt > 2 or ect > 2:
                    grid[i][j] = 0

            if grid[i][j] == 0:
                cnt = 0
                ect = 0
                try:
                    if grid[i+1][j] == 1: 
                        cnt += 1
                except IndexError:
                    ect += 1
                try:
                    if grid[i-1][j] == 1:
                        cnt += 1
                except IndexError:
                    ect += 1
                try:
                    if grid[i][j+1] == 1:
                        cnt += 1
                except IndexError:
                    ect += 1
                try:
                    if grid[i][j-1] == 1:
                        cnt += 1
                except IndexError:
                    ect += 1                
                if (cnt > 2 or ect > 2):
                    grid[i][j] = 1                
    return grid

def ConnectToContinent(grid,rng=1):
    ngrid = [[0 for i in range(0,len(grid[0]))] for j in range(0,len(grid))]
    for i in range(0,len(grid)):
        for j in range(0,len(grid[0])):
            if grid[i][j] == 0:
                for lr in range(-rng,rng+1):
                    for ud in range(-rng,rng+1):
                        if ud == 0 and lr == 0:
                            continue
                        try:
                            if grid[i+lr][j+ud] == 1 and i+lr >= 0 and j+ud >= 0:
                                ngrid[i][j] = 1
                                # testPoints2.append([i+lr,j+ud])
                                # testPoints.append([i,j])
                        except IndexError:
                            pass      
    for i in range(0,len(grid)):
        for j in range(0,len(grid[0])):
            if ngrid[i][j] == 1:
                if random.randint(0,1) == 1:
                    grid[i][j] = 1        
    return grid

def DiscreteGaussianDraw(mean, std):
    return int(random.gauss(mean,std))


def ConnectRandomPoints(grid):
    for i in range(0,len(grid)):
        for j in range(0,len(grid[0])):
            i = len(grid)-1-i #To my eye, the resulting map looks better if the points are connected from the bottom up
            j = len(grid[0])-1-j #Whereas top down looks biased towards the top. Not sure why.
            if grid[i][j] == 1:
                if random.randint(0,1) == 1:
                    grid[i][j] = 0
                    try:
                        grid[i+1][j] = 1
                    except IndexError:
                        pass
                    try:
                        grid[i-1][j] = 1
                    except IndexError:
                        pass
                    try:
                        grid[i][j+1] = 1
                    except IndexError:
                        pass
                    try:
                        grid[i][j-1] = 1
                    except IndexError:
                        pass
    return grid

def CountLand(grid):
    cnt = 0
    for i in range(0,len(grid)):
        for j in range(0,len(grid[0])):
            if grid[i][j] == 1:
                cnt += 1
    return cnt

def CreateGrid(x,y):
    grid = []
    for i in range(0,x):
        grid.append([])
        for j in range(0,y):
            grid[i].append(0)
    return grid


def ProgressBar(cnt, total, pct):
    cmd("cls")
    bar = ""
    cur = int(cnt/total/pct*100)/10
    for i in range(0,10):

        if i <= cur:
            bar += "==="
        else:
            bar += "   "
    if cur > 10:
        cur = 10
    print(f"[{bar}] {cur*10}% ({cnt}/{int(total*pct)})")

if __name__=="__main__":
    seed = int(datetime.now().timestamp())
    random.seed(seed)
    pctLand = 0.4
    n = 250
    totalMap = n*n
    rn = 500
    adrn = 10
    grid = CreateGrid(n,n)
    maxiter = 500
    iter = 0
    while True:    
        grid = AddRandomPointsToGrid(grid, rn)
        grid = ConnectRandomPoints(grid)
        grid = ChangeIsolatedPoints(grid)
        cnt = CountLand(grid)
        if cnt/totalMap >= pctLand:
            break
        else:
            # print(cnt/totalMap)
            rn = adrn
        ProgressBar(cnt, totalMap, pctLand)
        iter += 1
        if iter > maxiter:
            break
    ProgressBar(cnt, totalMap, pctLand)    
    print(f"Final: {cnt/totalMap}")    
    cnt = CountLand(grid)
    print(f"{cnt} vs {totalMap} is {cnt/totalMap}")
    plt.imshow(grid)
    plt.show(block=False)
    grid = ConnectToContinent(grid,rng=3)
    grid = ConnectRandomPoints(grid)
    grid = ChangeIsolatedPoints(grid)

    # print(testPoints)
    # print(testPoints2)
    # plt.scatter([i[0] for i in testPoints], [i[1] for i in testPoints]) 
    plt.figure()  
    plt.imshow(grid)
    plt.colorbar()
    plt.show()
    print(seed)

    plt.figure
    grid = AddRandomPointsToGrid(grid, rn, True, 0, 35)
    for i in range(0,6):
        grid = ConnectRandomPoints(grid)
    grid = ChangeIsolatedPoints(grid)
    plt.imshow(grid)
    plt.show(block=True)
    print(seed)

