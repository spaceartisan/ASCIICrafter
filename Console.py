# -*- coding: utf-8 -*-
"""
Console
=======
Console.py - This file contains the Console class and the Sound class. 
The Console class is used to draw the world and the Sound class is used to play sounds.
Additionally GetInput() is used to get input from the user. In the future these will be moved to their own files.

.. todo::
    Move GetInput() to its own file.
    Move Sound class to its own file.
    Add more sounds.
    Add more colors.
"""

from ctypes import create_unicode_buffer, windll
import curses
from sys import exit as ext
from os import listdir, remove
import msvcrt
from time import sleep
from os import system as cmd
import threading
import random

class Console:
    """
    Console class is used to draw the world and get input from the user.
    
    Parameters
    ----------
    world : World
        The world object that contains the map and entities.
    player : Player
        The player object that contains the player's information.
    sounds : Sound
        The sound object that contains the sounds
    """
    def __init__(self,world=None,player=None,sounds=None,firstRun=False):
        self.world = world
        self.player = player
        self.sounds = sounds
        self.StartCurses()
        self.statusTimerMax = 3
        self.statusTimerCur = 0
        self.menu = False
        self.menuPage = None
        self.ymax = 30
        self.xmax = 30
        self.load = None
        self.save = None
        self.saveMsg = None
        self.saveKeyPress = None
        self.confirmEnabled = False
        self.saveLoadTarget = None
        self.selectDelete = False
        self.typingEnabled = False
        self.typing = ""
        self.saveMetaName = ""
        self.getLoadsOnce = True
        self.loads = []
        self.firstRun = False
        self.action1 = "                    "
        self.action2 = "                    "
        self.stats = "                    "
        
    def StartCurses(self):
        """
        This function initializes curses and sets up the console.
        """
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
        """
        This function does nothing.
        """
        pass
        # mixer.music.play()
        
    def ResizeConsole(self,y,x):
        """
        This function resizes the console.
        **This function is not used.**
        """
        self.x, self.y = x,y
        
    def WorldRefresh(self,rate=0.1):
        """
        This function is threaded from ASCIICrafter.py and is the main loop to control the console.
        
        Parameters
        ----------
        rate : float
            The rate at which the world is drawn.
            
        """
        for i in range(0,1): #I'm ok with this solution. Using sleep seems wrong, but better than looping multiple times.
            curses.resize_term(0,0)
            self.stdscr.clear()
            self.stdscr.addstr(0,0,"Loading...")
            self.stdscr.refresh()
            sleep(1)
        self.stdscr.erase()
        self.stdscr.addstr(14,8*3,"Welcome to ASCIICrafter!")
        self.stdscr.addstr(15,8*3,"     Press any Key")
        self.stdscr.refresh()
        # self.sounds.pause = True
        input("")
        sleep(0.1)
        self.sounds.nbg = "sounds\\bg\\ab.mp3"
        self.sounds.st = 0
        sleep(0.1)
        while True:
            if self.world.exit:
                curses.endwin()
                cmd("cls")
                ext()
            y,x = self.stdscr.getmaxyx()
            resize = self.y != y or self.x != x
            if resize:                
                curses.resize_term(self.y, self.x)
                self.stdscr.clear()
                self.stdscr.refresh()
            else:
                if not self.menu:
                    self.DrawWorld()                        
                else:
                    self.DrawMenu(ky=self.menuPage)
                if self.statusTimerCur > 0:
                    self.statusTimerCur -= 0.1
                    if self.statusTimerCur <= 0:
                        self.DrawAction("                    ")
                        self.DrawAction2("                    ")
                        self.DrawStats("                    ")
            sleep(rate)
        print("WorldRefresh() exited.")
        
    def DrawAction(self,msg=None):
        """
        Draw the action message to the screen. Curser y position is 15.
        
        Parameters
        ----------
        msg : str
            The message to be displayed.
        """
        if msg != "               ":
            self.statusTimerCur = self.statusTimerMax
        self.stdscr.addstr(15,(self.xmax+1)*3,msg)
        self.action1 = msg

    def DrawAction2(self,msg=None):
        """
        Draw the action message to the screen. Curser y position is 17.
        
        Parameters
        ----------
        msg : str
            The message to be displayed.
        """
        if msg != "               ":
            self.statusTimerCur = self.statusTimerMax
        self.stdscr.addstr(17,(self.xmax+1)*3,msg)
        self.action2 = msg
        
    def DrawStats(self,msg=None):
        """
        Draw stats to the screen. Curser y position is 16.
        
        Parameters
        ----------
        msg : str
            The message to be displayed.
        """
        if msg != "               ":
            self.statusTimerCur = self.statusTimerMax
        self.stdscr.addstr(16,(self.xmax+1)*3,msg)
        self.stats = msg

    def GetLoads(self):
        """
        Gets the load files from the save folder.
        """
        load = []
        for file in listdir("saves"):
            if file.endswith(".save"):
                try:
                    num = int(file.split(".")[0])
                except ValueError:
                    continue
                if num > 0 and num < 10:
                    load.append(num)
        return load
    
    def GetSaveNames(self,ky):
        """
        Gets the save names from the save folder.
        
        Parameters
        ----------
        ky : int
            The number of the save file.
        """
        try:
            with open("saves/"+str(ky)+".save","rb") as f:
                rd = f.read(30)
        except FileNotFoundError:
            return "EMPTY"
        nm = rd.split(b"^v^v_v^v^")[0]
        try:
            nm = nm.decode()
        except UnicodeDecodeError:
            nm = "ERROR"
        return nm

    def DrawMenu(self, ky=None):
        self.channels = []
        channels = self.channels
        if True:
            self.stdscr.erase()
            self.redrawing = True
            ymx = self.ymax
            xmx = self.xmax
            snds = self.world.sounds
            if channels is not []:
                for chn in channels:
                    if not chn.is_alive():
                        channels.remove(chn)
            while len(snds) > 0 and len(channels) < 30:
                channels.append(threading.Thread(target=self.sounds.PlaySFX,args=(None,True,snds[0],)))
            if ky is None:
                self.stdscr.addstr(0,0,"Menu")
                self.stdscr.addstr(1,0,"1. New Game")
                self.stdscr.addstr(2,0,"2. Load Game")
                self.stdscr.addstr(3,0,"3. Save Game")
                self.stdscr.addstr(4,0,"4. Exit")
                self.stdscr.addstr(5,0,"5. Options")
                self.stdscr.refresh()
            elif ky == 1:
                self.stdscr.addstr(0,0,"New Game")
                self.stdscr.addstr(1,0,"1. Start")
                self.stdscr.addstr(2,0,"B. Back")
                self.stdscr.refresh()
            elif ky == 5:
                self.stdscr.addstr(0,0,"Options")
                self.stdscr.addstr(1,0,f"1. Sound: {self.sounds.sfxV}\\1000 Press A to increase and Z to decrease")
                self.stdscr.addstr(2,0,f"2. Music: {self.sounds.bgV}\\1000 Press S to increase and X to decrease")
                self.stdscr.addstr(3,0,"B. Back")
                self.stdscr.refresh()
            elif ky == 4:
                self.stdscr.addstr(0,0,"Exit")
                self.stdscr.addstr(1,0,"1. Yes")
                self.stdscr.addstr(2,0,"B. Back")
                self.stdscr.refresh()
            elif ky == 2:
                if self.selectDelete:
                    self.stdscr.addstr(0,0,"Delete Save")
                else:
                    self.stdscr.addstr(0,0,"Load Game")
                if self.getLoadsOnce:
                    self.loads = self.GetLoads()
                    self.getLoadsOnce = False
                for i in range(1,10):
                    if i in self.loads:
                        name = self.GetSaveNames(i)
                        if self.confirmEnabled and f"saves\\{i}.save" == self.saveLoadTarget:
                            self.stdscr.addstr(i,0,f"{i}. {name}", curses.A_STANDOUT)
                        else:
                            self.stdscr.addstr(i,0,f"{i}. {name}")
                    else:
                        self.stdscr.addstr(i,0,f"{i}. Empty")
                if not self.selectDelete:
                    self.stdscr.addstr(i+1,0,"D. Delete Save")
                    i += 1
                self.stdscr.addstr(i+1,0,"B. Back")
                if self.confirmEnabled:
                    self.stdscr.addstr(i+2,0,"Confirm Delete? Y/N")
                self.stdscr.refresh()
            elif ky == 3:
                self.stdscr.addstr(0,0,"Save Game")
                if self.getLoadsOnce:
                    self.loads = self.GetLoads()
                    self.getLoadsOnce = False
                for i in range(1,10):
                    if i in self.loads:
                        # name = self.GetSaveName(f"saves\\{i}.save")
                        name = self.GetSaveNames(i)
                        if self.confirmEnabled and f"saves\\{i}.save" == self.saveLoadTarget:
                            self.stdscr.addstr(i,0,f"{i}. {name}", curses.A_STANDOUT)
                        else:
                            self.stdscr.addstr(i,0,f"{i}. {name}")
                    else:
                        if self.confirmEnabled and f"saves\\{i}.save" == self.saveLoadTarget:
                            self.stdscr.addstr(i,0,f"{i}. New Save", curses.A_STANDOUT)
                        else:
                            self.stdscr.addstr(i,0,f"{i}. New Save")
                self.stdscr.addstr(i+1,0,"B. Back")
                if self.saveMsg is not None:
                    self.stdscr.addstr(i+2,0,self.saveMsg)
                if self.typingEnabled:
                    self.stdscr.addstr(i+2,0,f"Save name: {self.typing: <16}", curses.A_STANDOUT)
                    self.stdscr.addstr(i+3,0,"Press Enter to save")
                if self.confirmEnabled:
                    self.stdscr.addstr(i+2,0,f"Save name: {self.typing: <16}", curses.A_STANDOUT)
                    self.stdscr.addstr(i+3,0,"Confirm Save? Y/N")
                self.stdscr.refresh()

    def DrawWorld(self):
        """
        Draw the world to the screen. Is called by WorldRefresh. This function controls the drawing of the world. 
        It also controls the sounds.
        """
        self.channels = []
        channels = self.channels
        if True:
            # print(self.world.menu)
            self.stdscr.erase()
            self.redrawing = True
            ymx = self.ymax
            xmx = self.xmax
            snds = self.world.sounds
            if channels is not []:
                for chn in channels:
                    if not chn.is_alive():
                        channels.remove(chn)
            while len(snds) > 0 and len(channels) < 30:
                channels.append(threading.Thread(target=self.sounds.PlaySFX,args=(None,True,snds[0],)))#g
                channels[-1].start()
                snds.pop(0)
            wm = [x.copy() for x in self.world.wmap]
            for en in self.world.pdict["Enemy"]:
                try:
                    wm[en[1]][en[2]] = "U"
                except IndexError:
                    pass
            for pl in self.world.pdict["Player"]:
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
                    elif _ln == 9: #Bridge
                        ic = 'B'
                        bgcol = curses.color_pair(11) + curses.A_UNDERLINE + curses.A_BLINK
                    
                    try:
                        self.stdscr.addstr(15+i,(15+j)*3,f" {ic} ", bgcol)
                    except curses.error:
                        pass

            wxmx = 15
            wymx = 15
            self.redrawing = False
            self.stdscr.addstr(3,(wxmx*2+1)*3," ########################")
            self.stdscr.addstr(4,(wxmx*2+1)*3," #Ye Player Stats Here:##")
            self.stdscr.addstr(5,(wxmx*2+1)*3,f" #Health: {self.player.hp:03d}             #")
            self.stdscr.addstr(6,(wxmx*2+1)*3,f" #Wood: {self.player.WOOD:03d}             #")
            self.stdscr.addstr(7,(wxmx*2+1)*3,f" #Flowers: {self.player.PLANT:03d}          #")
            self.stdscr.addstr(8,(wxmx*2+1)*3,f" #Ore: {self.player.ORE:03d}              #")
            self.stdscr.addstr(9,(wxmx*2+1)*3,f" #Gems: {self.player.SPEC:03d}             #")
            self.stdscr.addstr(10,(wxmx*2+1)*3,f" #Exp: {self.player.EXP:03d}              #")
            self.stdscr.addstr(11,(wxmx*2+1)*3," ########################")
            
            self.stdscr.addstr(14,(wxmx*2+1)*3,f"  Last Action:")
            self.stdscr.addstr(15,(wxmx*2+1)*3,f"  {self.action1}")
            self.stdscr.addstr(16,(wxmx*2+1)*3,f"  {self.stats}")
            self.stdscr.addstr(17,(wxmx*2+1)*3,f"  {self.action2}")
            self.stdscr.addstr(wymx*2-1,(wxmx*2+1)*3,"")
            if self.saveKeyPress is not None:
                self.stdscr.addstr(20,(wxmx*2+1)*3,f"  {self.saveKeyPress}")
            self.stdscr.refresh()


class Sound():#Simple version of playsound with more commands!
    """
    Simple version of playsound with more commands!
    
    Parameters
    ----------
    bg : str
        The background music file to play
    """
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
        self.bgV = 600
        self.sfxV = 600
        
    def ChangeVolume(self,volume,background=False):
        """Change the volume of the sound
        
        Parameters
        ----------
        volume : int
            The volume to change to
        background : bool
            Whether to change the background music volume or not"""
        if background:
            self.bgV += volume
        else:
            self.sfxV += volume

        if self.bgV > 1000:
            self.bgV = 1000
        elif self.bgV < 0:
            self.bgV = 0
        if self.sfxV > 1000:
            self.sfxV = 1000
        elif self.sfxV < 0:
            self.sfxV = 0
    
    def Open(self,sd=None):
        """Open a file to play
        
        Parameters
        ----------
        sd : str
            The file to open"""
        if sd is None:
            sd = self.bg
        self.cs("open",sd)
        
    def Play(self,sd=None,repeat=False):
        """Play a file
        
        Parameters
        ----------
        sd : str
            The file to play
        repeat : bool
            Whether to repeat the file"""
        if sd is None:
            sd = self.bg
        # print(sd)
        if repeat:
            sd = sd + " repeat"
        # print(sd)
        self.cs("play",sd)
        
    def Pause(self,sd=None):
        """Pause a file
        
        Parameters
        ----------
        sd : str
            The file to pause
        """
        if sd is None:
            sd = self.bg
        self.cs("pause",sd)
    
    def PlaySFX(self,sdfx=None,wait=True,numb=None):
        """Play a sound effect
        
        Parameters
        ----------
        sdfx : str
            The file to play
        wait : bool
            Whether to wait for the file to finish playing
        numb : int
            The number of the file to play
        """
        if numb is not None:
            sdfx = self.files[numb]
        elif sdfx == None:
            sdfx = self.bg
        # print(sdfx, numb)
        self.Open(sdfx)
        self.cs2(f"setaudio {sdfx} volume to {self.sfxV}")
        if wait:
            self.cs2(f"play {sdfx} wait")
        else:
            self.cs2(f"play {sdfx}")
        self.Close(sdfx)
        
    def Seek(self,sdfx,ms):
        """Seek to a position in a file
        
        Parameters
        ----------
        sdfx : str
            The file to seek
        ms : int
            The position to seek to in milliseconds
        """
        print("Seeking")
        self.Open(sdfx)
        self.cs2(f"set {sdfx} time format milliseconds")
        self.cs2(f"seek {sdfx} to {ms}")
        self.Play(sdfx)
        sleep(20)
        self.Close(sdfx)
        
    def Volume(self,volume,sd=None):
        """Change the volume of a file
        
        Parameters
        ----------
        volume : int
            The volume to change to
        sd : str
            The file to change the volume of
        """
        print("Hello my sound " + str(volume) + "  " + str(sd))
        if sd is None:
            sd = self.bg
        self.cs2(f"setaudio {sd} volume to {volume}")
    
    def Stop(self,sd=None):
        """Stop a file
        
        Parameters
        ----------
        sd : str
            The file to stop
        """
        if sd is None:
            sd = self.bg
        self.cs("stop",sd)
        
    def Close(self,sd=None):
        """Close a file
        
        Parameters
        ----------
        sd : str
            The file to close
        """
        if sd is None:
            sd = self.bg
        self.cs("close",sd)
        
    def PlayBG(self):
        """Play the background music"""
        bgV = self.bgV
        while True:
            if self.bgV != bgV:
                self.Volume(volume=self.bgV)
                bgV = self.bgV
            if self.st == 0 or (self.st == 2 and not self.pause):
                if self.st != 2:
                    self.Close()
                    if self.nbg is not None:
                        self.bg = self.nbg
                        self.nbg = self.bg
                    cmd("cls")
                    print(f"Now playing {self.bg}")
                self.Open()
                self.Volume(volume=self.bgV)
                self.Play(repeat=True)
                self.st = 1
            elif self.st == 1 and self.pause:
                self.Pause()
                print("pause")
                self.bgV = 150
                self.st = 2
            if self.ex == 1:
                self.Close()
                break
        # self.Close()
        print("Exit sounds")

def WorldKeyPresses(world, player, x, y, console, ky):
    px = x
    py = y
    if ky == 'w':
        x -= 1
    elif ky == 'a':
        y -= 1
    elif ky == "s":
        x += 1
    elif ky == "d":
        y += 1
    elif ky == " ":
        ic = world.wmap[x][y]
        console.DrawAction(f"  Destroying {ic}     ")
        player.Action(harvest=True,nm=ic,x=x,y=y)
        if player.hstats is not None:
            console.DrawStats(f"  Health: {player.hstats[0]}  ")
        else:
            console.DrawStats(f"  Health: 0  ")
    elif ky == "u":
        curses.flash()
    elif ky == "p":
        console.sounds.pause = not console.sounds.pause
    elif ky == "b":
        ic = world.wmap[x][y]
        if ic in [1,2,3,4]:
            console.DrawAction(f"  Can't build on {ic} ")
        else:
            # console.DrawAction(f"  Building W ")
            rtn = player.Action(build=True,nm=ic,x=x,y=y)
            if rtn:
                console.DrawAction(f"  Building W      ")
            else:
                console.DrawAction("  Not enough wood  ")
    elif ky in ["H","K","P","M"]:
        player.Action(fight=True,nm=ky,x=x,y=y)

    player.PosUpdate(x,y)
    if px != x or py != y:
        player.CancelAction()

def MenuKeyPresses(world, console, ky):
    if console.menuPage is None:
        isFirst = True
        if ky == "5":
            console.menuPage = 5
        elif ky == "4":
            console.menuPage = 4
        elif ky == "3":
            console.menuPage = 3
        elif ky == "2":
            console.menuPage = 2
        elif ky == "1":
            console.menuPage = 1
    else:
        isFirst = False
    # elif ky == "2":
    #     console.menuPage = 2
    # elif ky == "1":
    #     console.menuPage = 1
    if not isFirst:
        if console.menuPage == 5:
            if ky == "s":
                console.sounds.ChangeVolume(10,True)
            elif ky == "x":
                console.sounds.ChangeVolume(-10,True)
            elif ky == "a":
                console.sounds.ChangeVolume(10,False)
            elif ky == "z":
                console.sounds.ChangeVolume(-10,False)
        elif console.menuPage == 4:
            if ky == "1":
                world.fullExit = True
                world.exit = True
                ext()
        elif console.menuPage == 1:
            if ky == "1":
                world.exit = True
                ext()
        elif console.menuPage == 2:
            loads = console.GetLoads()
            kys = ["1","2","3","4","5","6","7","8","9"]
            nkys = [nk for nk in kys if int(nk) in loads]
            if ky in nkys:
                if console.selectDelete:
                    if not console.confirmEnabled:
                        console.saveLoadTarget = f"saves\\{ky}.save"
                        console.confirmEnabled = True
                    # remove(f"saves\\{ky}.save")
                    # console.selectDelete = False
                    # console.saveMsg = None
                else:
                    console.load = f"saves\\{ky}.save"
                    world.exit = True
                    ext()
            elif ky == "d" or ky == "D":
                if not console.selectDelete:
                    console.selectDelete = True
            elif ky == "y" or ky == "Y":
                if console.confirmEnabled:
                    while True:
                        try:
                            remove(console.saveLoadTarget)
                            break
                        except PermissionError:
                            pass
                    console.saveLoadTarget = None
                    console.selectDelete = False
                    console.confirmEnabled = False
                    console.getLoadsOnce = True
                    console.saveMsg = f"Deleted save {ky}"
            elif ky == "n" or ky == "N":
                if console.confirmEnabled:
                    console.confirmEnabled = False
        elif console.menuPage == 3:
            loads = console.GetLoads()
            kys = ["1","2","3","4","5","6","7","8","9"]
            if ky in kys and not console.typingEnabled and not console.confirmEnabled:
                if not console.typingEnabled and not console.confirmEnabled:
                    console.typingEnabled = True
                    console.typing = ""
                    console.saveLoadTarget = f"saves\\{ky}.save"
            elif console.typingEnabled:
                if ky.encode() == b'\r':
                    console.saveMetaName = console.typing
                    console.typingEnabled = False                    
                    console.confirmEnabled = True
                else:
                    GetInputString(console,ky)
            elif ky == "y" or ky == "Y":
                if console.confirmEnabled:
                    console.saveMsg = None
                    console.save = console.saveLoadTarget
                    console.saveLoadTarget = None
                    console.saveMsg = f"Saved {console.save}"
                    console.selectDelete = False
                    console.confirmEnabled = False
                    console.saveMetaName = console.typing
                    console.typing = ""
                    console.getLoadsOnce = True
                    console.stdscr.refresh()
            elif ky == "n" or ky == "N":
                if console.confirmEnabled:
                    console.confirmEnabled = False
        if console.menuPage is not None:
            if (ky == "b" or ky == "B") and not console.selectDelete and not console.confirmEnabled and not console.typingEnabled:
                console.menuPage = None
                console.saveMsg = None
                console.getLoadsOnce = True
            elif (ky == "b" or ky == "B") and console.selectDelete and not console.confirmEnabled and not console.typingEnabled:
                console.selectDelete = False
                console.confirmEnabled = False
                console.getLoadsOnce = True

def GetInputString(console,ky):
    """Get input from the user and act on it.
    This is a blocking function, so it should be run in a separate thread.
    
    Args:
        console (Console): The console object
    """ 
    lowerAlpha = [chr(i) for i in range(97,123)]
    upperAlpha = [chr(i) for i in range(65,91)]
    if ky in lowerAlpha or ky in upperAlpha:
        console.typing += ky
    elif ky.encode() == b'\x08':
        console.typing = console.typing[:-1]

def GetInput(world,player,console,ts):
    """Get input from the user and act on it.
    This is a blocking function, so it should be run in a separate thread.
    
    Args:
        world (World): The world object
        player (Player): The player object
        console (Console): The console object
        ts (float): The sound thread (deprecated)
    """ 
    kyn = 0
    while True:  
        if msvcrt.kbhit():         
            pressed = msvcrt.getch()
            # console.saveKeyPress = f"{pressed} key press number {kyn}"
            # print(f"{pressed} key press number {kyn}")
            # kyn += 1
            # continue
            # if pressed == b'\x1b':
            #     world.exit = True
            #     ext()
            for ply in world.pdict["Player"]: #I don't think this is the best way to do this, but it works for now (Already have reference to player)
                if ply[0].consoleMsg is not None:
                    console.DrawAction2(ply[0].consoleMsg)
                    ply[0].consoleMsg = None
                if ply[0].ids == player:
                    try:
                        ky = pressed.decode()
                        x = ply[1]
                        y = ply[2]
                        # print(ply)
                        if not console.menu:
                            WorldKeyPresses(world, ply[0], x, y, console, ky)
                        elif console.menu:
                            MenuKeyPresses(world, console, ky)                           
                        if ky == "m" and not console.typingEnabled and not console.confirmEnabled:
                            console.menu = not console.menu
                    except UnicodeDecodeError:
                        pass
            world.UpdateWorld(pOnly=True)
