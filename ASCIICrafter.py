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
# import numpy as np

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
        
    def CreateWorld(self):
        for n,i in enumerate(self.wmap):
            for m,_i in enumerate(i):
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
        for _ in range(0,8):
            self.CreateRandomHollowBox(mx=8,mn=3)

    def CreateRandomHollowBox(self,mx=None,mn=None):
        x = int(rnd()*(self.xmax - self.xmin))
        y = int(rnd()*(self.ymax - self.ymin))
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
                    self.wmap[i][j] = 6

    def AlterWorld(self,x,y,nm):
        self.wmap[x][y] = nm
    
    def AddPlayer(self,player,x=None,y=None):
        wm = self.wmap
        if x is None:
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
                if wm[x][y] != 6:
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
                    if pl[1] >= self.xmax or pl[2] >= self.ymax or pl[1] < 0 or pl[2] < 0 or self.wmap[pl[1]][pl[2]] == 6:
                        pl[1] = prevx
                        pl[2] = prevy
                        self.sounds.append(3)
        if not pOnly:
            for en in self.pdict["Enemy"]:
                # print(en)
                prevx, prevy = en[1],en[2] 
                x,y = en[0].UpdateBehavior(en[1],en[2])
                en[1] = x
                en[2] = y
                if x >= self.xmax or y>= self.ymax or x < 0 or y < 0 or self.wmap[x][y] == 6:
                    en[1],en[2] = prevx, prevy
                    
                
    


class Console:
    def __init__(self,world=None,player=None,sounds=None):
        self.world = world
        self.player = player
        self.sounds = sounds
        self.StartCurses()
        self.statusTimerMax = 3
        self.statusTimerCur = 0
        self.ymax = self.world.ymax
        self.xmax = self.world.xmax
        
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
        self.y, self.x = self.world.ymax,self.world.xmax*4
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
                        self.DrawStats("                    ")
            sleep(rate)
        
    def DrawAction(self,msg=None):
        if msg != "               ":
            self.statusTimerCur = self.statusTimerMax
        self.stdscr.addstr(15,(self.xmax+1)*3,msg)
        
    def DrawStats(self,msg=None):
        if msg != "               ":
            self.statusTimerCur = self.statusTimerMax
        self.stdscr.addstr(16,(self.xmax+1)*3,msg)
        
    def DrawWorld(self):
        self.channels = []
        channels = self.channels
        if True:
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
            for nm, ln in enumerate(wm):
                row = ''
                for nm2,_ln in enumerate(ln):
                    if _ln == 0:
                        ic = ','
                        bgcol = curses.color_pair(1)
                    elif _ln == 1:
                        bgcol = curses.color_pair(2)#stdscr.addstr(0,0,"Pretty text", curses.color_pair(1))
                        ic = ';'
                    elif _ln == 2:
                        bgcol = curses.color_pair(3)
                        ic = 'T'
                    elif _ln == 3:
                        bgcol = curses.color_pair(4)
                        ic = 'M'
                    elif _ln == 4:
                        bgcol = curses.color_pair(5)
                        ic = '@'
                    elif _ln == 6:
                        ic = 'W'
                        bgcol = curses.color_pair(8) + curses.A_STANDOUT
                    elif _ln == "X":
                        ic = '&'
                        bgcol = curses.color_pair(6)
                    elif _ln == "U":
                        ic = '&'
                        bgcol = curses.color_pair(7)
                    elif _ln == 5:
                        ic = ' '
                        bgcol = curses.color_pair(1)
                    
                    # if nm2 == 0:
                    self.stdscr.addstr(nm,nm2*3,f" {ic} ", bgcol)
                    # else:
                        # stdscr.addstr(f" {ic} ", bgcol)
          
            self.redrawing = False
            self.stdscr.addstr(4,(xmx+1)*3," ########################")
            self.stdscr.addstr(5,(xmx+1)*3," #Ye Player Stats Here:##")
            self.stdscr.addstr(6,(xmx+1)*3,f" #Wood: {self.player.WOOD:03d}             #")
            self.stdscr.addstr(7,(xmx+1)*3,f" #Flowers: {self.player.PLANT:03d}          #")
            self.stdscr.addstr(8,(xmx+1)*3,f" #Ore: {self.player.ORE:03d}              #")
            self.stdscr.addstr(9,(xmx+1)*3,f" #Gems: {self.player.SPEC:03d}             #")
            self.stdscr.addstr(10,(xmx+1)*3," ########################")
            
            self.stdscr.addstr(14,(xmx+1)*3,f"  Last Action:")
            self.stdscr.addstr(ymx-1,(xmx)*3,"")
            self.stdscr.refresh()

def GetInput(world,player,console,ts): 
    while True:  
        if msvcrt.kbhit():         
            pressed = msvcrt.getch()
            if pressed == b'\x1b':
                world.exit = True
                ext()
            for ply in world.pdict["Player"]:
                if ply[0].ids == player:
                    try:
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
                            console.DrawAction(f"  Destroying {ic}")
                            ply[0].Action(harvest=True,nm=ic,x=ply[1],y=ply[2])
                            if ply[0].hstats is not None:
                                console.DrawStats(f"  Health: {ply[0].hstats[0]}  ")
                            else:
                                console.DrawStats(f"  Health: 0  ")
                        elif ky == "u":
                            curses.flash()
                            # console.ResizeConsole(25,120)
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
                                    console.DrawAction(f"  Building W ")
                                else:
                                    console.DrawAction("  Not enough wood")
                        ply[0].PosUpdate(x,y)
                        if ply[1] != x or ply[2] != y:
                            ply[0].CancelAction()
                    except UnicodeDecodeError:
                        pass
            world.UpdateWorld(pOnly=True)
        
        # if not world.redrawing:
        #     world.DrawWorld()

class Player:
    WOOD = 0
    PLANT = 0
    ORE = 0
    SPEC = 0
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
    
    def Cooldown(self,id=None,tm=None):
        self.cooldown[id] = True
        sleep(tm)
        self.cooldown[id] = False

    def UpdateInventory(self,ty=None,amt=None):
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
            t1 = threading.Thread(target=self.Cooldown,args=(0,0.5,))
            t1.start()
            if self.hstats[0] <= 0:
                self.UpdateInventory(self.hstats[1],1)
                self.world.AlterWorld(x,y,5)
                self.CancelAction()
        if build is not None:
            if self.cooldown[0]:
                return
            if self.WOOD >= 1:
                self.UpdateInventory(0,-1)
                self.world.AlterWorld(x,y,6)
                self.world.sounds.append(4)
                t1 = threading.Thread(target=self.Cooldown,args=(0,0.5,))
                t1.start()
                return True
            else:
                return False
    
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
        fil = ["a","b","c","d","e","f","g"]#a,d,g
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
    simplify = False
    n = 30
    sounds = Sound("sounds\\bg\\ab.mp3")
    if not simplify:
        ts = threading.Thread(target=sounds.PlayBG,args=())
        ts.start()
    world = World(0,n,0,n) #Needs to be same height and width because I mixed up x and y. Kinda a deep fix...
    world.CreateWorld()
    player = Player(123456,world)
    console = Console(world,player,sounds)
    world.AddPlayer(player)
    for i in range(5):
        world.AddEnemy(Enemy(world))
    if not simplify:
        t1 = threading.Thread(target=GetInput,args=(world,123456,console,ts,))    
        t1.start()
        t2 = threading.Thread(target=console.WorldRefresh,args=(0.001,))    
        t2.start()
    init = False
    console.DrawWorld()
    while True:
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

    
