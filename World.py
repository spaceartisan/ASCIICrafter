# -*- coding: utf-8 -*-
"""
World
=====
World.py - Contains the World and Island classes. This script is used to generate the world.

.. todo::
    Consider fixing the x,y coordinates. They are currently backwards.
"""



from math import cos, sin
from random import random as rnd
import random
from os import system as cmd


class World:
    """
    This class is used to generate the world.
    
    Parameters
    ----------
    xmin : int
        The minimum x value of the world.
    xmax : int 
        The maximum x value of the world.
    ymin : int
        The minimum y value of the world.
    ymax : int
        The maximum y value of the world.
    """
    def __init__(self,xmin=0,xmax=2,ymin=0,ymax=2):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.time = 8.0
        self.wmap = [[0 for _j in range(xmin,xmax)] for _k in range(ymin,ymax)]
        self.pdict = {"Player" : [], "Enemy" : []}
        self.menu = False
        self.exit = False
        self.fullExit = False
        self.sounds = []
        self.atk = []
        self.saveName = None

        
    def CreateWorld(self,grid=None,buildings=None):
        """Creates the world.
        
        Parameters
        ----------
        grid : list
            The grid to use.
        """
        if grid is not None:
            self.wmap = grid
        for n,i in enumerate(self.wmap):
            for m,_i in enumerate(i):
                if self.wmap[n][m] == 7:
                    continue
                rndVal = rnd()
                if rndVal < 0.65:
                    continue
                elif rndVal < 0.85:
                    self.wmap[n][m] = 1 #Plant
                elif rndVal < 0.95:
                    self.wmap[n][m] = 2 #Tree
                elif rndVal < 0.98:
                    self.wmap[n][m] = 3 #Ore
                else:
                    self.wmap[n][m] = 4 #Special
        # self.CreateRandomHollowBox()
        if buildings is None:
            return
        for _ in range(0,buildings):
            self.CreateRandomHollowBox2(mx=15,mn=5)

    def CreateRandomHollowBox2(self,mx=None,mn=None):
        """Creates a random hollow box. The resulting box will deconflict with other boxes.
        
        Parameters
        ----------
        mx : int
            The maximum size of the box.
        mn : int
            The minimum size of the box.
        """
        maxiter = 500
        iter = 0
        while True:
            while True:
                x = int(rnd()*(self.xmax - self.xmin))
                y = int(rnd()*(self.ymax - self.ymin))
                if self.wmap[x][y] != 7:
                    break    
            if mx is None or mn is None:
                w = int(rnd()*(self.xmax - self.xmin))
                h = int(rnd()*(self.ymax - self.ymin))
            else:
                w = int(rnd()*(mx - mn)) + mn
                h = int(rnd()*(mx - mn)) + mn        
            if x + 2 >= self.xmax:
                x = self.xmax - 3
            if y + 2 >= self.ymax:
                y = self.ymax - 3
            if w < 3:
                w = 3
            if h < 3:
                h = 3
            doesIsSucceed = True
            for i in range(x-1,x+h+1):
                for j in range(y-1,y+w+1):
                    if i < 0 or j < 0 or i >= self.xmax or j >= self.ymax:
                        doesIsSucceed = False
                    elif self.wmap[i][j] == 6 or self.wmap[i][j] == 8 or self.wmap[i][j] == 7:
                        doesIsSucceed = False
                    if not doesIsSucceed:
                        break
                if not doesIsSucceed:
                    break
            if doesIsSucceed:
                break
            else:
                iter += 1
                if iter > maxiter:
                    return

        self.CreateHollowBox2(x,y,w,h)

    def CreateRandomHollowBox(self,mx=None,mn=None):
        """Creates a random hollow box.
        
        Parameters
        ----------
        mx : int
            The maximum size of the box.
        mn : int
            The minimum size of the box.
        """
        while True:
            x = int(rnd()*(self.xmax - self.xmin))
            y = int(rnd()*(self.ymax - self.ymin))
            if self.wmap[x][y] != 7:
                break    
        if mx is None or mn is None:
            w = int(rnd()*(self.xmax - self.xmin))
            h = int(rnd()*(self.ymax - self.ymin))
        else:
            w = int(rnd()*(mx - mn)) + mn
            h = int(rnd()*(mx - mn)) + mn        
        if x + 2 >= self.xmax:
            x = self.xmax - 3
        if y + 2 >= self.ymax:
            y = self.ymax - 3
        if w < 3:
            w = 3
        if h < 3:
            h = 3
        self.CreateHollowBox(x,y,w,h)

    def CreateHollowCircle(self,x,y,r):
        """Creates a hollow circle.
        
        Parameters
        ----------
        x : int
            The x coordinate of the circle.
        y : int
            The y coordinate of the circle.
        r : int
            The radius of the circle.
        """
        pi = 3.1415926
        for ang in range(0,360):
            _x = int(x + r * cos(ang*pi/180))#pi = 
            _y = int(y + r * sin(ang*pi/180))
            if _x < 0:
                _x = 0
            if _x >= self.xmax:
                _x = self.xmax - 1
            if _y < 0:
                _y = 0
            if _y >= self.ymax:
                _y = self.ymax - 1
            self.wmap[_x][_y] = 6


    def CreateHollowBox(self,x,y,w,h): #Wow I need to fix the coordinates, there will be a future issue with this
        """Creates a hollow box. Called from CreateRandomHollowBox.
        
        Parameters
        ----------
        x : int
            The x coordinate of the box.
        y : int
            The y coordinate of the box.
        w : int
            The width of the box.
        h : int
            The height of the box.

        """
        if x+h >= self.ymax:
            h = self.ymax - x
        if y+w >= self.xmax:
            w = self.xmax - y
        for i in range(x,x+h):
            for j in range(y,y+w):
                if i == x or i == x+h-1 or j == y or j == y+w-1:
                    if self.wmap[i][j] == 7: #Water
                        pass
                    else:
                        self.wmap[i][j] = 6 #Wall
                else:
                    if self.wmap[i][j] == 7: #Water
                        pass
                    else:
                        self.wmap[i][j] = 8 #Floor
        for i in range(x,x+h):
            for j in range(y,y+w):
                if self.wmap[i][j] == 8:
                    for _i in range(i-1,i+2):
                        for _j in range(j-1,j+2):
                            if _i < 0 or _j < 0 or _i >= self.ymax or _j >= self.xmax:
                                continue
                            if self.wmap[_i][_j] == 7:
                                self.wmap[_i][_j] = 6
        for i in range(x,x+h):
            for j in range(y,y+w):
                if self.wmap[i][j] == 6:
                    wc = 0
                    fc = 0
                    oc = 0
                    bc = 0
                    for _i in range(i-1,i+2):
                        for _j in range(j-1,j+2):
                            if _i == i and _j == j:
                                continue
                            if _i < 0 or _j < 0 or _i >= self.ymax or _j >= self.xmax:
                                bc += 1
                                continue
                            if self.wmap[_i][_j] == 6:
                                wc += 1
                            elif self.wmap[_i][_j] == 8:
                                fc += 1
                            else:
                                oc += 1
                    if wc > 2 and oc == 0 and bc == 0 and fc > 0:
                        self.wmap[i][j] = 8
                    elif fc == 0:
                        self.wmap[i][j] = 0

    def CreateHollowBox2(self,x,y,w,h): #Wow I need to fix the coordinates, there will be a future issue with this
        """Creates a hollow box. Called from CreateRandomHollowBox2.
        
        Parameters
        ----------
        x : int
            The x coordinate of the box.
        y : int
            The y coordinate of the box.
        w : int
            The width of the box.
        h : int
            The height of the box.
        """
        if x+h >= self.ymax:
            h = self.ymax - x
        if y+w >= self.xmax:
            w = self.xmax - y
        for i in range(x,x+h):
            for j in range(y,y+w):
                if i == x or i == x+h-1 or j == y or j == y+w-1:
                    if self.wmap[i][j] == 7: #Water
                        pass
                    else:   
                        self.wmap[i][j] = 6 #Wall
                else:
                    if self.wmap[i][j] == 7: #Water
                        pass
                    else:
                        self.wmap[i][j] = 8 #Floor
        side = random.randint(0,3)
        if side == 0: #LEFT
            self.wmap[x+3][y] = 5
        elif side == 1: #BOTTOM
            self.wmap[x+h-1][y+3] = 5
        elif side == 2: #RIGHT
            self.wmap[x+h-4][y+w-1] = 5
        elif side == 3: #TOP
            self.wmap[x][y+w-4] = 5


    def AlterWorld(self,x,y,nm):
        """Alters the world map at a given coordinate.
        
        Parameters
        ----------
        x : int
            The x coordinate of the box.
        y : int
            The y coordinate of the box.
        nm : int
            The new value of the coordinate.
        """
        self.wmap[x][y] = nm
    
    def AddPlayer(self,player,x=None,y=None):
        """Adds a player to the world.
        
        Parameters
        ----------
        player : Player
            The player to be added.
        x : int
            The x coordinate of the player.
        y : int
            The y coordinate of the player.
        """
        wm = self.wmap
        if x is None:
            # x = int(rnd()*(self.xmax - self.xmin))
            # y = int(rnd()*(self.ymax - self.ymin))
            x = int(self.xmax/2)
            y = int(self.ymax/2)
            while True:                
                if wm[x][y] != 6 and wm[x][y] != 7:
                    break
                x = int(rnd()*(self.xmax - self.xmin))
                y = int(rnd()*(self.ymax - self.ymin))
            trn = wm[x][y]
            player.PosUpdate(x,y)
            player.initx = x
            player.inity = y
            self.pdict["Player"].append([player,x,y,trn])
        else:
            trn = wm[x][y]
            player.PosUpdate(x,y)
            self.pdict["Player"].append([player,x,y,trn])
            
    def AddEnemy(self,enemy,x=None,y=None):
        """Adds an enemy to the world.
        
        Parameters
        ----------
        enemy : Enemy
            The enemy to be added.
        x : int
            The x coordinate of the enemy.
        y : int
            The y coordinate of the enemy.
        """
        wm = self.wmap
        if x is None:
            while True:
                x = int(rnd()*(self.xmax - self.xmin))
                y = int(rnd()*(self.ymax - self.ymin))
                if wm[x][y] != 6 and wm[x][y] != 7:
                    break
            trn = wm[x][y]
            self.pdict["Enemy"].append([enemy,x,y,trn])
        else:
            trn = wm[x][y]
            self.pdict["Enemy"].append([enemy,x,y,trn])
            
    def UpdateWorld(self, pOnly=False, eOnly=False):
        """Updates the world.
        
        Parameters
        ----------
        pOnly : bool
            If True, only updates the player.
        eOnly : bool
            If True, only updates the enemy.
        """
        if not eOnly:
            for pl in self.pdict["Player"]:
                if pl[0].px is not None or pl[0].py is not None:
                    prevx, prevy = pl[1], pl[2]
                    pl[1] = pl[0].px
                    pl[2] = pl[0].py
                    pl[0].ClearPUpdate()
                    if pl[1] >= self.xmax or pl[2] >= self.ymax or pl[1] < 0 or pl[2] < 0 or self.wmap[pl[1]][pl[2]] == 6 or self.wmap[pl[1]][pl[2]] == 7:
                        pl[1] = prevx
                        pl[2] = prevy
                        self.sounds.append(3)
                        
        if not pOnly:
            for en in self.pdict["Enemy"]:
                # print(en)
                if self.atk != []:
                    if self.atk[0] == en[1] and self.atk[1] == en[2]:
                        self.sounds.append(12)
                        self.atk[-1].GainExperience(50)
                        self.pdict["Enemy"].remove(en)
                        continue
                prevx, prevy = en[1],en[2] 
                x,y = en[0].UpdateBehavior(en[1],en[2])
                en[1] = x
                en[2] = y
                if x >= self.xmax or y>= self.ymax or x < 0 or y < 0 or self.wmap[x][y] == 6 or self.wmap[x][y] == 7:
                    en[1],en[2] = prevx, prevy
            self.atk = []
                    
                
class Island:
    """
    The Island class is used to help generate the world map. It is used to generate the world map and to generate the world map's terrain.
    """
    def AddRandomPointsToGrid(grid, numPoints, gauss=False, mean=0, std=0, frac=1):
        """Adds random points to a grid.
        
        Parameters
        ----------
        grid : list
            The grid to add points to.
        numPoints : int
            The number of points to add.
        gauss : bool
            If True, the points will be added in a gaussian distribution.
        mean : int
            The mean of the gaussian distribution.
        std : int
            The standard deviation of the gaussian distribution.

        Returns
        -------
        list
            The grid with the points added.
        xmin : int
            The minimum x value of the points.
        xmax : int
            The maximum x value of the points.
        ymin : int
            The minimum y value of the points.
        ymax : int
            The maximum y value of the points.

        """
        for i in range(0,numPoints):
            if frac != 1:
                xm = int(round(len(grid)*(1-frac)/2))
                ym = int(round(len(grid[0])*(1-frac)/2))
                xmin = xm
                xmax = len(grid)-xm
                ymin = ym
                ymax = len(grid[0])-ym
            else:
                xmin = 0
                xmax = len(grid)
                ymin = 0
                ymax = len(grid[0])
            if gauss == False:
                x = random.randint(xmin,xmax-1)
                y = random.randint(ymin,ymax-1)
            else:
                while True:
                    nn = 15
                    x = Island.DiscreteGaussianDraw(mean,std)+int(len(grid)/2)
                    y = Island.DiscreteGaussianDraw(mean,std)+int(len(grid[0])/2)
                    if x >= nn and y >= nn and x <= len(grid)-nn and y <= len(grid[0])-nn:
                        break
            try:
                grid[x][y] = 1
            except IndexError:
                pass
        return grid, xmin, xmax, ymin, ymax

    def ChangeIsolatedPoints(grid, xmin=None, xmax=None, ymin=None, ymax=None):
        """Changes isolated points to water or grass depending on the adjacent tiles.
        
        Parameters
        ----------
        grid : list
            The grid to change.
        
        Returns
        -------
        list
            The changed grid.
        """
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
        """Connects the island to the continent.
        
        Parameters
        ----------
        grid : list
            The grid to connect.
        rng : int
            The range of the connection.

        Returns
        -------
        list
            The connected grid.
        """
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
        """Draws a random number from a discrete gaussian distribution.
        
        Parameters
        ----------
        mean : int
            The mean of the gaussian distribution.
        std : int
            The standard deviation of the gaussian distribution.

        Returns
        -------
        int
            The random number.
        """
        return int(random.gauss(mean,std))

    def ConvertGrid(grid):
        """Will convert a grid of 0s and 1s to a grid of 7s and 0s.
        
        Parameters
        ----------
        grid : list
            The grid to convert.

        Returns
        -------
        list
            The converted grid.
        """
        for i in range(0,len(grid)):
            for j in range(0,len(grid[0])):
                if grid[i][j] == 0:
                    grid[i][j] = 7
                else:
                    grid[i][j] = 0
        return grid

    def ConnectRandomPoints(grid, xmin=None, xmax=None, ymin=None, ymax=None):
        """Connects random points together to form islands.
        
        Parameters
        ----------
        grid : list
            The grid to connect.
        xmin : int
            The minimum x value.
        xmax : int
            The maximum x value.
        ymin : int
            The minimum y value.
        ymax : int
            The maximum y value.

        Returns
        -------
        list
            The connected grid.
        """
        for i in range(xmin,xmax):
            for j in range(ymin,ymax):
                i = ymax-1-i #To my eye, the resulting map looks better if the points are connected from the bottom up
                j = ymax-1-j #Whereas top down looks biased towards the top. Not sure why.
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
        """Counts the number of land tiles in a grid.
        
        Parameters
        ----------
        grid : list
            The grid to count.

        Returns
        -------
        int
            The number of land tiles.
        """
        cnt = 0
        for i in range(0,len(grid)):
            for j in range(0,len(grid[0])):
                if grid[i][j] == 1:
                    cnt += 1
        return cnt

    def CreateGrid(x,y):
        """Creates a grid of 0s.
        
        Parameters
        ----------
        x : int
            The width of the grid.
        y : int
            The height of the grid.

        Returns
        -------
        list
            The grid of 0s.
        """
        grid = []
        for i in range(0,x):
            grid.append([])
            for j in range(0,y):
                grid[i].append(0)
        return grid


    def ProgressBar(cnt, total, pct):
        """Creates a progress bar.
        
        Parameters
        ----------
        cnt : int
            The current count.
        total : int
            The total count.
        pct : float
            The percentage of the total count to display.
        """
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
        print(f"Generating world - [{bar}] {cur*10}% ({cnt}/{int(total*pct)})")    