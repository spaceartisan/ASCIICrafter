# -*- coding: utf-8 -*-
"""
Entities
========
Entities.py - This file contains the Player and Enemy classes. 

.. todo::
    Add more enemies.
    Add more enemy types.
    Add more enemy AI.
    Add robust player inventory.
"""

from time import sleep
import threading
import random
from Object import WorldObjects, Item
from math import atan2, degrees, pi, radians

class Player:
    """
    This class contains the player's stats and methods.
    
    Parameters
    ----------
    ids : int
        The player's ID.
    world : World
        The world that the player is in.
    """
    WOOD = 0
    PLANT = 0
    ORE = 0
    SPEC = 0
    EXP = 0
    def __init__(self,ids=None,world=None, initx=None, inity=None):
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
        self.initx = None
        self.inity = None
        self.cdown = 0.25
    
    def Cooldown(self,id=None,tm=None):
        """Sets a cooldown for the player's actions.
        
        Parameters
        ----------
        id : int
            The ID of the action.
        tm : float
            The time to wait before the cooldown is over.
        """
        self.cooldown[id] = True
        sleep(tm)
        self.cooldown[id] = False

    def GainExperience(self,amt=None):
        """Gains experience for the player.
        
        Parameters
        ----------
        amt : int
            The amount of experience to gain.
        """
        self.consoleMsg = f"  Gained {amt} EXP  "
        self.EXP += amt
        # if self.EXP >= 100:
        #     self.EXP -= 100
        #     self.LevelUp()

    def UpdateInventory(self,ty=None,amt=None,playSound=True):
        """Updates the player's inventory.
        
        Parameters
        ----------
        ty : int
            The type of item to update.
        amt : int
            The amount to update.
        playSound : bool
            Whether or not to play a sound.
        """
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
        """Performs an action for the player.
        
        Parameters
        ----------
        harvest : bool
            Whether or not to harvest.
        craft : bool
            Whether or not to craft.
        build : bool
            Whether or not to build.
        fight : bool
            Whether or not to fight.
        nm : str
            The name of the object to interact with.
        x : int
            The x position of the object to interact with.
        y : int
            The y position of the object to interact with.
        """
        if harvest is not None and nm not in [0,5]:
            if self.cooldown[0]:
                return
            if self.harvest == False:
                self.harvest = True
                if WorldObjects.ReturnObj(nm) == None:
                    self.harvest = False
                    return
                self.hstats = [x for x in WorldObjects.ReturnObj(nm)]
            self.hstats[0] -= 1
            self.world.sounds.append(0)
            if self.hstats[0] <= 0:
                self.UpdateInventory(self.hstats[1],1)
                self.world.AlterWorld(x,y,5)
                self.CancelAction()
            else:
                t1 = threading.Thread(target=self.Cooldown,args=(0,self.cdown,))
                t1.start()
        if build is not None:
            if self.cooldown[0]:
                return
            if self.WOOD >= 1:
                self.UpdateInventory(0,-1)
                self.world.AlterWorld(x,y,6)
                self.world.sounds.append(4)
                t1 = threading.Thread(target=self.Cooldown,args=(0,self.cdown,))
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
            if x >= self.world.xmax or y >= self.world.ymax or x < 0 or y < 0:
                return
            if self.world.wmap[x][y] == 6:
                self.world.AlterWorld(x,y,5)
                self.world.sounds.append(4)
                self.UpdateInventory(0,1,False)
                t1 = threading.Thread(target=self.Cooldown,args=(0,self.cdown,))
                t1.start()
            elif self.world.wmap[x][y] == 7:
                if self.WOOD >= 1 and self.ORE >= 1:
                    self.UpdateInventory(0,-1)
                    self.UpdateInventory(2,-1)
                    self.world.AlterWorld(x,y,9)
                    self.world.sounds.append(4)
                    t1 = threading.Thread(target=self.Cooldown,args=(0,self.cdown,))
                    t1.start()
            elif self.world.wmap[x][y] == 9:
                self.UpdateInventory(0,1,False)
                self.UpdateInventory(2,1, False)
                self.world.AlterWorld(x,y,7)
                self.world.sounds.append(4)
                t1 = threading.Thread(target=self.Cooldown,args=(0,self.cdown,))
                t1.start()
            else:
                self.world.atk = [x,y,self]
                self.world.sounds.append(0)
                t1 = threading.Thread(target=self.Cooldown,args=(0,self.cdown,))
                t1.start()

    def DealDamage(self,amt=None):
        """Deals damage to the player.
        
        Parameters
        ----------
        amt : int
            The amount of damage to deal.
        """
        self.hp -= amt
        if self.hp <= 0:
            self.world.sounds.append(7)
            self.hp = 10
            self.PosUpdate(self.initx,self.inity)
        else:
            self.world.sounds.append(0)
    
    def CancelAction(self):
        """Cancels the player's current action."""
        if self.harvest:
            self.harvest = False
            self.hstats = None
    
    def PosUpdate(self,x,y):
        """Updates the player's position.
        
        Parameters
        ----------
        x : int
            The x position to update to.
        y : int
            The y position to update to.
        """
        # if x < 0:
        #     x = 0
        # if y < 0:
        #     y = 0
        if self.cooldown[1]:
            return
        self.px = x
        self.py = y
        
    def ClearPUpdate(self):
        """Clears the player's position update."""
        self.px = None
        self.py = None
        t2 = threading.Thread(target=self.Cooldown, args=(1,self.cdown,))
        t2.start()

class Enemy:
    """
    This class contains the enemy's stats and methods.
    
    Parameters
    ----------
    world : World
        The world that the enemy is in.
    """
    def __init__(self,world=None):
        self.world = world
        self.hp = 0
        self.spd = 2
        self.lastDir = 0
        self.radius = 10
        self.delay = 1
        self.dcount = 0

    def Aggro(self,x,y):
        """Checks if the enemy is in range of the player.
        
        Parameters
        ----------
        x : int
            The x position of the enemy.
        y : int
            The y position of the enemy.

        Returns
        -------
        bool
            Whether or not the enemy is in range of the player.
        """
        pl, px, py, tr = self.world.pdict['Player'][0]
        if pl is not None:
            if pl.hp > 0:
                if abs(px - x) <= self.radius and abs(py - y) <= self.radius: # 0 deg is down positive is counter clockwise
                    enemyToPlayer = atan2(py - y, px - x)
                    if enemyToPlayer > 0 and enemyToPlayer <= radians(90):
                        quad = 1 # bottom right
                    elif enemyToPlayer > radians(90) and enemyToPlayer <= radians(180):
                        quad = 2 # top right
                    elif enemyToPlayer > -radians(90) and enemyToPlayer <= 0:
                        quad = 4 # bottom left
                    elif enemyToPlayer > -radians(180) and enemyToPlayer <= -radians(90):
                        quad = 3 # top left
                    try:
                        bup = self.world.wmap[x-1][y] == 6 or self.world.wmap[x-1][y] == 7
                    except:
                        bup = False
                    try:
                        bdown = self.world.wmap[x+1][y] == 6 or self.world.wmap[x+1][y] == 7
                    except:
                        bdown = False
                    try:
                        bleft = self.world.wmap[x][y-1] == 6 or self.world.wmap[x][y-1] == 7
                    except:
                        bleft = False
                    try:
                        bright = self.world.wmap[x][y+1] == 6 or self.world.wmap[x][y+1] == 7
                    except:
                        bright = False
                    if (abs(py - y) == 0 and abs(px - x) == 1) or (abs(py - y) == 1 and abs(px - x) == 0):
                        return False, 0, True, pl
                    if enemyToPlayer <= radians(45) and enemyToPlayer > -radians(45): # PLayer is below enemy
                        # print(f"q:{quad} bup:{bup} bdown:{bdown} bleft:{bleft} bright:{bright} enemyToPlayer:{degrees(enemyToPlayer)}")
                        val = 1
                        if quad == 1 and bdown:
                            val = 2
                        elif quad == 4 and bdown:
                            val = 4
                        return True, val, False, None 
                    elif enemyToPlayer <= radians(135) and enemyToPlayer > radians(45):# Player is right of enemy
                        val = 2
                        # print(f"q:{quad} bup:{bup} bdown:{bdown} bleft:{bleft} bright:{bright} enemyToPlayer:{degrees(enemyToPlayer)}")
                        if quad == 1 and bright:
                            val = 1
                        elif quad == 2 and bright:
                            val = 3
                        return True, val, False, None 
                    elif enemyToPlayer <= -radians(45) and enemyToPlayer > -radians(135): # Player is left of enemy
                        # print(f"q:{quad} bup:{bup} bdown:{bdown} bleft:{bleft} bright:{bright} enemyToPlayer:{degrees(enemyToPlayer)}")
                        val = 4
                        if quad == 3 and bleft:
                            val = 3
                        elif quad == 4 and bleft:
                            val = 1
                        return True, val, False, None
                    else: # Player is above enemy
                        # print(f"q:{quad} bup:{bup} bdown:{bdown} bleft:{bleft} bright:{bright} enemyToPlayer:{degrees(enemyToPlayer)}")
                        val = 3
                        if quad == 2 and bup:
                            val = 2
                        elif quad == 3 and bup:
                            val = 4
                        return True, val, False, None
        return False, 0, False, None

    def UpdateBehavior(self,x,y):
        """Updates the enemy's behavior.
        
        Parameters
        ----------
        x : int
            The x position of the enemy.
        y : int
            The y position of the enemy.

        Returns
        -------
        x : int
            The updated x position of the enemy.
        y : int
            The updated y position of the enemy.
        """
        if self.dcount >= self.delay:
            seePlayer, newDir, attack, pl = self.Aggro(x,y)
            if attack:
                pl.DealDamage(2)
                self.dcount = 0
                return x,y
            if seePlayer:
                self.lastDir = newDir
            else:
                self.lastDir = random.randint(1,4)
            ld = self.lastDir
            if ld == 1:
                x += 1 #Go down
            elif ld == 2:
                y += 1 #Go right
            elif ld == 3:
                x -= 1 #Go up
            elif ld == 4:
                y -= 1  #Go left
            if self.lastDir == 4:
                self.lastDir = 0
            self.dcount = 0
            if x < 0:
                x = 0
            if y < 0:
                y = 0
        else:
            # sleep(0.1)
            self.dcount += 0.1
        return x,y