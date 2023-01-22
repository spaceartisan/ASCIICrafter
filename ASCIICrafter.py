# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 12:15:58 2023

@author: wclif
"""
from math import cos, sin
from random import random as rnd
from os import system as cmd
import msvcrt
import random
import threading
from time import sleep
import curses
from sys import exit as ext
from ctypes import create_unicode_buffer, windll

class WorldObjects:
    TREE = [5,0]
    FLOWER = [1,1]
    MINE = [10,2]
    SPEC = [15,3]
    def ReturnObj(objNm):
        if objNm == 2:
            return WorldObjects.TREE
        elif objNm == 1:
            return WorldObjects.FLOWER
        elif objNm == 3:
            return WorldObjects.MINE
        elif objNm == 4:
            return WorldObjects.SPEC

class World:
    def __init__(self,xmin=0,xmax=2,ymin=0,ymax=2):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.time = 8.0
        self.wmap = [[0 for _j in range(xmin,xmax)] for _k in range(ymin,ymax)]
        self.pdict = {"Player" : [], "Enemy" : []}
        self.exit = False
        self.sounds = []
        self.atk = []
        
    def CreateWorld(self,grid=None):
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
        for _ in range(0,50):
            self.CreateRandomHollowBox2(mx=15,mn=5)

    def CreateRandomHollowBox2(self,mx=None,mn=None):
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
        self.wmap[x][y] = nm
    
    def AddPlayer(self,player,x=None,y=None):
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
            self.pdict["Player"].append([player,x,y,trn])
        else:
            trn = wm[x][y]
            player.PosUpdate(x,y)
            self.pdict["Player"].append([player,x,y,trn])
            
    def AddEnemy(self,enemy,x=None,y=None):
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
    def AddRandomPointsToGrid(grid, numPoints, gauss=False, mean=0, std=0):
        for i in range(0,numPoints):
            if gauss == False:
                x = random.randint(0,len(grid)-1)
                y = random.randint(0,len(grid[0])-1)
            else:
                while True:
                    nn = 40
                    x = Island.DiscreteGaussianDraw(mean,std)+int(len(grid)/2)
                    y = Island.DiscreteGaussianDraw(mean,std)+int(len(grid[0])/2)
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

    def ConvertGrid(grid):
        for i in range(0,len(grid)):
            for j in range(0,len(grid[0])):
                if grid[i][j] == 0:
                    grid[i][j] = 7
                else:
                    grid[i][j] = 0
        return grid

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
        print(f"Generating world - [{bar}] {cur*10}% ({cnt}/{int(total*pct)})")    


class Console:
    def __init__(self,world=None,player=None,sounds=None):
        self.world = world
        self.player = player
        self.sounds = sounds
        self.StartCurses()
        self.statusTimerMax = 3
        self.statusTimerCur = 0
        self.ymax = 30
        self.xmax = 30
        
    def StartCurses(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(10, curses.COLOR_CYAN, curses.COLOR_CYAN)
        curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        # self.y, self.x = self.world.ymax,self.world.xmax*4
        self.y, self.x = 30,30*4
        if self.y < 18:
            self.y = 18
        if self.x < 21*3+25:
            self.x = 21*3+25 
        curses.resize_term(self.y, self.x)
        
        # mixer.init()
        # mixer.music.load('bag.mp3')
        
        
    def PlaySound(self):
        pass
        # mixer.music.play()
        
    def ResizeConsole(self,y,x):
        self.x, self.y = x,y
        
    def WorldRefresh(self,rate=0.1):
        while True:
            if world.exit:
                ext()
            curses.resize_term(0,0)
            y,x = self.stdscr.getmaxyx()
            resize = self.y != y or self.x != x
            if resize:                
                curses.resize_term(self.y, self.x)
                self.stdscr.clear()
                self.stdscr.refresh()
            else:
                self.DrawWorld()
                if self.statusTimerCur > 0:
                    self.statusTimerCur -= 0.1
                    if self.statusTimerCur <= 0:
                        self.DrawAction("                    ")
                        self.DrawAction2("                    ")
                        self.DrawStats("                    ")
            sleep(rate)
        
    def DrawAction(self,msg=None):
        if msg != "               ":
            self.statusTimerCur = self.statusTimerMax
        self.stdscr.addstr(15,(self.xmax+1)*3,msg)

    def DrawAction2(self,msg=None):
        if msg != "               ":
            self.statusTimerCur = self.statusTimerMax
        self.stdscr.addstr(17,(self.xmax+1)*3,msg)
        
    def DrawStats(self,msg=None):
        if msg != "               ":
            self.statusTimerCur = self.statusTimerMax
        self.stdscr.addstr(16,(self.xmax+1)*3,msg)
        
    def DrawWorld(self):
        self.channels = []
        channels = self.channels
        if True:
            # self.stdscr.erase()
            self.redrawing = True
            ymx = self.ymax
            xmx = self.xmax
            snds = world.sounds
            if channels is not []:
                for chn in channels:
                    if not chn.is_alive():
                        channels.remove(chn)
            while len(snds) > 0 and len(channels) < 30:
                channels.append(threading.Thread(target=self.sounds.PlaySFX,args=(None,True,snds[0],)))#g
                channels[-1].start()
                snds.pop(0)
            wm = [x.copy() for x in self.world.wmap]
            for en in world.pdict["Enemy"]:
                try:
                    wm[en[1]][en[2]] = "U"
                except IndexError:
                    pass
            for pl in world.pdict["Player"]:
                try:
                    wm[pl[1]][pl[2]] = "X"
                except IndexError:
                    pass
            # print('\033[4A\033[2K', end='')
            # print()
            # print()
            # for nm, ln in enumerate(wm):
            _x = pl[1]
            _y = pl[2]

            for i in range(-int(xmx/2),int(xmx/2)+1):
                row = ''
                # for nm2,_ln in enumerate(ln):
                for j in range(-int(ymx/2),int(ymx/2)+1):
                    if _x + i < 0 or _y + j < 0 or _x + i >= len(wm) or _y + j >= len(wm[0]):
                        _ln = 99
                    else:
                        _ln = wm[_x+i][_y+j]
                    if _ln == 0: #Grass
                        ic = ','
                        bgcol = curses.color_pair(1)
                    elif _ln == 1: #Flower
                        bgcol = curses.color_pair(2)#stdscr.addstr(0,0,"Pretty text", curses.color_pair(1))
                        ic = ';'
                    elif _ln == 2: #Tree
                        bgcol = curses.color_pair(3)
                        ic = 'T'
                    elif _ln == 3:#Ore
                        bgcol = curses.color_pair(4)
                        ic = 'M'
                    elif _ln == 4: #Special
                        bgcol = curses.color_pair(5)
                        ic = '@'
                    elif _ln == 6: #Wall
                        ic = 'W'
                        bgcol = curses.color_pair(8) + curses.A_STANDOUT
                    elif _ln == "X": #Player
                        ic = '&'
                        bgcol = curses.color_pair(6)
                    elif _ln == "U": #Enemy
                        ic = '&'
                        bgcol = curses.color_pair(7)
                    elif _ln == 5: #Blank Grass
                        ic = ' '
                        bgcol = curses.color_pair(1)
                    elif _ln == 99: #Blank
                        ic = ' '
                        bgcol = curses.color_pair(9)
                    elif _ln == 7: #Water
                        ric = random.randint(0,10)
                        if ric == 0:
                            ic = '~'
                        elif ric == 1:
                            ic = '-'
                        else:
                            ic = ' '
                        bgcol = curses.color_pair(10) + curses.A_STANDOUT
                    elif _ln == 8: #Floor
                        ic = '|'
                        bgcol = curses.color_pair(11) + curses.A_UNDERLINE + curses.A_BLINK
                    
                    try:
                        self.stdscr.addstr(15+i,(15+j)*3,f" {ic} ", bgcol)
                    except curses.error:
                        pass

            wxmx = 15
            wymx = 15
            self.redrawing = False
            self.stdscr.addstr(4,(wxmx*2+1)*3," ########################")
            self.stdscr.addstr(5,(wxmx*2+1)*3," #Ye Player Stats Here:##")
            self.stdscr.addstr(6,(wxmx*2+1)*3,f" #Wood: {self.player.WOOD:03d}             #")
            self.stdscr.addstr(7,(wxmx*2+1)*3,f" #Flowers: {self.player.PLANT:03d}          #")
            self.stdscr.addstr(8,(wxmx*2+1)*3,f" #Ore: {self.player.ORE:03d}              #")
            self.stdscr.addstr(9,(wxmx*2+1)*3,f" #Gems: {self.player.SPEC:03d}             #")
            self.stdscr.addstr(10,(wxmx*2+1)*3,f" #Exp: {self.player.EXP:03d}              #")
            self.stdscr.addstr(11,(wxmx*2+1)*3," ########################")
            
            self.stdscr.addstr(14,(wxmx*2+1)*3,f"  Last Action:")
            self.stdscr.addstr(wymx*2-1,(wxmx*2+1)*3,"")
            self.stdscr.refresh()

def GetInput(world,player,console,ts): 
    while True:  
        if msvcrt.kbhit():         
            pressed = msvcrt.getch()
            if pressed == b'\x1b':
                world.exit = True
                ext()
            for ply in world.pdict["Player"]: #I don't think this is the best way to do this, but it works for now (Already have reference to player)
                if ply[0].consoleMsg is not None:
                    console.DrawAction2(ply[0].consoleMsg)
                    ply[0].consoleMsg = None
                if ply[0].ids == player:
                    try:
                        if pressed == b'\xe0': #U,L,D,R : H, K, P, M
                            pressed = msvcrt.getch()
                            if pressed.decode() not in ["H","K","P","M"]:
                                continue
                        ky = pressed.decode()
                        x = ply[1]
                        y = ply[2]
                        # print(ply)
                        if ky == 'w':
                            x -= 1
                        elif ky == 'a':
                            y -= 1
                        elif ky == "s":
                            x += 1
                        elif ky == "d":
                            y += 1
                        elif ky == " ":
                            ic = world.wmap[ply[1]][ply[2]]
                            console.DrawAction(f"  Destroying {ic}     ")
                            ply[0].Action(harvest=True,nm=ic,x=ply[1],y=ply[2])
                            if ply[0].hstats is not None:
                                console.DrawStats(f"  Health: {ply[0].hstats[0]}  ")
                            else:
                                console.DrawStats(f"  Health: 0  ")
                        elif ky == "u":
                            curses.flash()
                        elif ky == "p":
                            console.sounds.pause = not console.sounds.pause
                        elif ky == "b":
                            ic = world.wmap[ply[1]][ply[2]]
                            if ic in [1,2,3,4]:
                                console.DrawAction(f"  Can't build on {ic} ")
                            else:
                                # console.DrawAction(f"  Building W ")
                                rtn = ply[0].Action(build=True,nm=ic,x=ply[1],y=ply[2])
                                if rtn:
                                    console.DrawAction(f"  Building W      ")
                                else:
                                    console.DrawAction("  Not enough wood  ")
                        elif ky in ["H","K","P","M"]:
                            ply[0].Action(fight=True,nm=ky,x=ply[1],y=ply[2])
                        ply[0].PosUpdate(x,y)
                        if ply[1] != x or ply[2] != y:
                            ply[0].CancelAction()
                    except UnicodeDecodeError:
                        pass
            world.UpdateWorld(pOnly=True)

class Player:
    WOOD = 0
    PLANT = 0
    ORE = 0
    SPEC = 0
    EXP = 0
    def __init__(self,ids=None,world=None):
        self.world = world
        self.hp = 10
        self.axe = 0
        self.paxe = 0
        self.swrd = 0 
        self.ids = ids
        self.px = None
        self.py = None
        self.harvest = False
        self.hstats = None
        self.cooldown = [False,False] #Harves, Movement
        self.consoleMsg = None
    
    def Cooldown(self,id=None,tm=None):
        self.cooldown[id] = True
        sleep(tm)
        self.cooldown[id] = False

    def GainExperience(self,amt=None):
        self.consoleMsg = f"  Gained {amt} EXP  "
        self.EXP += amt
        # if self.EXP >= 100:
        #     self.EXP -= 100
        #     self.LevelUp()

    def UpdateInventory(self,ty=None,amt=None,playSound=True):
        if ty == 0:
            if self.WOOD < 100-amt:
                self.WOOD += amt
        if ty == 1:
            if self.PLANT < 100-amt:
                self.PLANT += amt
        if ty == 2:
            if self.ORE < 100-amt:
                self.ORE += amt
        if ty == 3:
            if self.SPEC < 100-amt:
                self.SPEC += amt
        if amt > 0:
            if playSound:
                self.world.sounds.append(6)
    
    def Action(self,harvest=None,craft=None,build=None,fight=None,nm=None,x=None,y=None):
        if harvest is not None and nm not in [0,5]:
            if self.cooldown[0]:
                return
            if self.harvest == False:
                self.harvest = True
                self.hstats = [x for x in WorldObjects.ReturnObj(nm)]
            self.hstats[0] -= 1
            self.world.sounds.append(0)
            if self.hstats[0] <= 0:
                self.UpdateInventory(self.hstats[1],1)
                self.world.AlterWorld(x,y,5)
                self.CancelAction()
            else:
                t1 = threading.Thread(target=self.Cooldown,args=(0,0.35,))
                t1.start()
        if build is not None:
            if self.cooldown[0]:
                return
            if self.WOOD >= 1:
                self.UpdateInventory(0,-1)
                self.world.AlterWorld(x,y,6)
                self.world.sounds.append(4)
                t1 = threading.Thread(target=self.Cooldown,args=(0,0.35,))
                t1.start()
                return True
            else:
                return False
        if fight is not None:
            if self.cooldown[0]:
                return
            if nm == "H":
                x -= 1
            elif nm == "K":
                y -= 1
            elif nm == "P":
                x += 1
            elif nm == "M":
                y += 1
            if self.world.wmap[x][y] == 6:
                self.world.AlterWorld(x,y,5)
                self.world.sounds.append(4)
                self.UpdateInventory(0,1,False)
                t1 = threading.Thread(target=self.Cooldown,args=(0,0.35,))
                t1.start()
            else:
                self.world.atk = [x,y,self]
                self.world.sounds.append(0)
                t1 = threading.Thread(target=self.Cooldown,args=(0,0.35,))
                t1.start()


    
    def CancelAction(self):
        if self.harvest:
            self.harvest = False
            self.hstats = None
    
    def PosUpdate(self,x,y):
        # if x < 0:
        #     x = 0
        # if y < 0:
        #     y = 0
        if self.cooldown[1]:
            return
        self.px = x
        self.py = y
        
    def ClearPUpdate(self):
        self.px = None
        self.py = None
        t2 = threading.Thread(target=self.Cooldown, args=(1,0.2,))
        t2.start()

class Enemy:
    def __init__(self,world=None):
        self.world = world
        self.hp = 0
        self.spd = 2
        self.lastDir = 0
        self.radius = 10
        self.delay = 1
        self.dcount = 0
        

    def UpdateBehavior(self,x,y):
        if self.dcount >= self.delay:
            self.lastDir = random.randint(1,4)
            ld = self.lastDir
            if ld == 1:
                x += 1
            elif ld == 2:
                y += 1
            elif ld == 3:
                x -= 1
            elif ld == 4:
                y -= 1
            if self.lastDir == 4:
                self.lastDir = 0
            self.dcount = 0
            if x < 0:
                x = 0
            if y < 0:
                y = 0
        else:
            self.dcount += 0.1
        return x,y
                     
class Sound():#Simple version of playsound with more commands!
    def __init__(self,bg):
        self.bg = bg
        self.nbg = None
        self.ex = 0
        self.st = 0 # 0 not playing, 1 playing, 2 paused
        self.pause = False
        bufLen = 600
        buf = create_unicode_buffer(bufLen)
        self.cs = lambda c, s : windll.winmm.mciSendStringW(f"{c} {s}", buf, bufLen - 1,0)
        self.cs2 = lambda c : windll.winmm.mciSendStringW(f"{c}", buf, bufLen - 1,0)
        self.isPlayer = True
        dire = "sounds\\sfx\\"
        dirb = "sounds\\bg\\"
        ext = ".mp3"
        fil = ["a","b","c","d","e","f","g","h","i","j","k","l","m"]#a,d,g,m
        fib = ["ab","bb","cb","db","eb"]
        self.files = [f"{dire}{fn}{ext}" for fn in fil]
        self.fileb = [f"{dirb}{fn}{ext}" for fn in fib]
        
    def Open(self,sd=None):
        if sd is None:
            sd = self.bg
        self.cs("open",sd)
        
    def Play(self,sd=None,repeat=False):
        if sd is None:
            sd = self.bg
        # print(sd)
        if repeat:
            sd = sd + " repeat"
        print(sd)
        self.cs("play",sd)
        
    def Pause(self,sd=None):
        if sd is None:
            sd = self.bg
        self.cs("pause",sd)
    
    def PlaySFX(self,sdfx=None,wait=True,numb=None):
        if numb is not None:
            sdfx = self.files[numb]
        elif sdfx == None:
            sdfx = self.bg
        print(sdfx, numb)
        self.Open(sdfx)
        if wait:
            self.cs2(f"play {sdfx} wait")
        else:
            self.cs2(f"play {sdfx}")
        self.Close(sdfx)
        
    def Seek(self,sdfx,ms):
        print("Seeking")
        self.Open(sdfx)
        self.cs2(f"set {sdfx} time format milliseconds")
        self.cs2(f"seek {sdfx} to {ms}")
        self.Play(sdfx)
        sleep(20)
        self.Close(sdfx)
        
    def Stop(self,sd=None):
        if sd is None:
            sd = self.bg
        self.cs("stop",sd)
        
    def Close(self,sd=None):
        if sd is None:
            sd = self.bg
        self.cs("close",sd)
        
    def PlayBG(self):
        while True:
            if self.st == 0 or (self.st == 2 and not self.pause):
                if self.st != 2:
                    self.Close()
                    if self.nbg is not None:
                        self.bg = self.nbg
                        self.nbg = self.bg
                    cmd("cls")
                    print(f"Now playing {self.bg}")
                self.Open()
                self.Play(repeat=True)
                self.st = 1
            elif self.st == 1 and self.pause:
                self.Pause()
                print("pause")
                self.st = 2
            if self.ex == 1:
                break
        # self.Close()
        print("Exit sounds")
            


   

if __name__ == "__main__":
    cmd('cls')
    # random.seed(1236489)
    simplify = False #This is used for debugging purposes.
    sounds = Sound("sounds\\bg\\ab.mp3")
    
    #Needs to be same height and width because I mixed up x and y. Kinda a deep fix...
    # world.CreateWorld()
    # print("Loading map")
    ##########################################################################
    # Island Generation
    ##########################################################################
    pctLand = 0.4
    n = 200
    totalMap = n*n
    rn = 100
    adrn = 10
    maxiter = 500
    iter = 0
    itype = 2
    world = World(0,n,0,n) 
    if itype == 0:
        world.CreateWorld()
    elif itype == 1:
        grid = Island.CreateGrid(n,n)
        grid = Island.AddRandomPointsToGrid(grid, rn, True, 0, 15)
        for i in range(0,6):
            grid = Island.ConnectRandomPoints(grid)
        grid = Island.ChangeIsolatedPoints(grid)
    elif itype == 2:
        grid = Island.CreateGrid(n,n)
        while True:  
            print()  
            grid = Island.AddRandomPointsToGrid(grid, rn)
            grid = Island.ConnectRandomPoints(grid)
            grid = Island.ChangeIsolatedPoints(grid)
            cnt = Island.CountLand(grid)
            if cnt/totalMap >= pctLand:
                break
            else:
                rn = adrn
            iter += 1
            if iter > maxiter:
                break
            Island.ProgressBar(cnt,totalMap,pctLand)
        grid = Island.ConnectToContinent(grid,rng=3)
        grid = Island.ConnectRandomPoints(grid)
        grid = Island.ChangeIsolatedPoints(grid)
        Island.ProgressBar(cnt,totalMap,pctLand)
    if itype != 0:
        world.CreateWorld(grid=Island.ConvertGrid(grid))    
    ##########################################################################
    if not simplify:
        ts = threading.Thread(target=sounds.PlayBG,args=())
        ts.start()
    player = Player(123456,world)
    console = Console(world,player,sounds)
    world.AddPlayer(player)
    for i in range(200):
        world.AddEnemy(Enemy(world))
    if not simplify:
        t1 = threading.Thread(target=GetInput,args=(world,123456,console,ts,))    
        t1.start()
        t2 = threading.Thread(target=console.WorldRefresh,args=(0.001,))    
        t2.start()
    else:
        console.DrawWorld()
    init = False
    while True:
        if not simplify:
            world.UpdateWorld(eOnly=init,pOnly=False)
        if world.exit:
            break
        sleep(0.1)
    sounds.ex = 1
    sounds.pause = True
    if not simplify:
        t1.join()
        t2.join()
        ts.join()
        for chn in console.channels:
                chn.join()
    cmd('cls')
    cmd("ECHO Thank you for playing!    ...TeeHee")
    cmd('pause')

    
