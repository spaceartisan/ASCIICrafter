# -*- coding: utf-8 -*-
"""
Entities.py - This file contains the Player and Enemy classes. 
"""

from time import sleep
import threading
import random
from Object import WorldObjects, Item

class Player:
    #Inventory 
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