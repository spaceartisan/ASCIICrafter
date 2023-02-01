# -*- coding: utf-8 -*-
"""
ASCIICrafter
============
This is the top level main file. It is used to run the game.
Here you can configure the game's settings. This includes the world size, the world type, and the player's starting position.

Bug List
--------
- When the player dies, if he is moving, his position will not reset to the spawn point.
- In the menu->save, after saving, sometimes the adjacent save will not be shown
- In the menu->save doesn't load the save name sometimes after save.
- Not really a bug, but probably bad practice. On menu save/load redraw, all files are reread, this could be slow. (In progress)
- Screen does not fully draw sometimes, don't know how to force the bug. (The AI thinks it's because the screen is not fully cleared. I should investigate this.)
- Despite having a cooldown timer, the movements are inconsistent if the player holds down a key.
- When the sound starts at the same time as the first DrawWorld, the curses will not be drawn
"""

from os import system as cmd
from time import sleep, time
import threading
import sys
import argparse
import random
import pickle

from Console import Console, Sound, GetInput
from Entities import Player, Enemy
from World import World, Island
   

def parseInput():
    """
    This function parses the input from the user. It takes in a string and returns a list of the words in the string.

    Parameters
    ----------
    input : str
        The string to be parsed.

    Returns
    -------
    size : int
        The size of the world.
    enemyAmt : int
        The number of enemies to spawn.

    Examples
    --------
    >>> python ASCIICrafter.py -n 10 -e 5
    10, 5
    """

    size = 100
    enemyAmt = 50
    seed = None
    save = None
    load = None
    buildings = 25

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--Size", help="Size of world (n*n)")
    parser.add_argument("-e", "--EnemyAmt", help="Number of enemies")
    parser.add_argument("-d", "--Seed", help="Seed for world generation")
    parser.add_argument("-s", "--Save", help="Save file name")
    parser.add_argument("-l", "--Load", help="Load file name")
    parser.add_argument("-b", "--Building", help="Number of buildings")
    parser.add_argument("-D", "--Debug", help="Debug mode")
    args = parser.parse_args()
    if args.Size:
        size = int(args.Size)
    if args.EnemyAmt:
        enemyAmt = int(args.EnemyAmt)
    if args.Seed:
        seed = int(args.Seed)
    if args.Save:
        save = args.Save
    if args.Load:
        load = args.Load
    if args.Building:
        buildings = int(args.Building)

    return size, enemyAmt, seed, save, load, buildings


def saveWorld(world, filename, saveName="Blank"):
    """
    This function saves the world and player to a file.

    Parameters
    ----------
    world : World
        The world to be saved.
    filename : str
        The name of the file to be saved to.
    """
    if world.saveName is None:
        world.saveName = saveName
    print(world.saveName)
    with open(filename, "wb") as f:
        f.write(f"{saveName}^v^v_v^v^".encode())

    with open(filename, "ab") as f:
        pickle.dump(world, f)




def loadWorld(filename):
    """
    This function loads the world and player from a file.

    Parameters
    ----------
    filename : str
        The name of the file to be loaded from.
    """
    with open(filename, "rb") as f:
        hold = f.read()
        hold = hold.split(b"^v^v_v^v^")[1]

    with open(filename, "wb") as f:
        f.write(hold)

    with open(filename, "rb") as f:
        world = pickle.load(f)

    saveWorld(world, filename, world.saveName)
    return world


def NewWorld(n, enemySpawn, seed, save, load, buildings, simplify, firstRun):
    sounds = Sound("sounds\\bg\\eb.mp3")
    console = Console(firstRun=firstRun)
    #Needs to be same height and width because I mixed up x and y. Kinda a deep fix...
    # world.CreateWorld()
    # print("Loading map")
    ##########################################################################
    # Island Generation
    ##########################################################################

    if seed is not None:
        random.seed(seed)
    if firstRun:
        world = World(0,1,0,1)
        firstRun = False
        console.world = world
        console.sounds = sounds
    elif load is None:
        # enemySpawn = 0
        pctLand = 0.25
        # n = 10
        totalMap = n*n
        rn = 100
        adrn = 10
        maxiter = 500
        iter = 0
        itype = 2
        world = World(0,n,0,n) 
        if itype == 0:
            world.CreateWorld(buildings=buildings)
        elif itype == 1:
            grid = Island.CreateGrid(n,n)
            grid, xmin, xmax, ymin, ymax = Island.AddRandomPointsToGrid(grid, rn, True, 0, 15)
            for i in range(0,6):
                grid = Island.ConnectRandomPoints(grid, xmin, xmax, ymin, ymax)
            grid = Island.ChangeIsolatedPoints(grid, xmin, xmax, ymin, ymax)
        elif itype == 2:
            grid = Island.CreateGrid(n,n)
            while True:   
                grid, xmin, xmax, ymin, ymax = Island.AddRandomPointsToGrid(grid, rn, frac=0.6)
                grid = Island.ConnectRandomPoints(grid, xmin, xmax, ymin, ymax)
                grid = Island.ChangeIsolatedPoints(grid, xmin, xmax, ymin, ymax)
                cnt = Island.CountLand(grid)
                if cnt/totalMap >= pctLand and cnt/totalMap <= pctLand+0.05:
                    break
                else:
                    rn = adrn
                iter += 1
                if iter > maxiter:
                    break
                Island.ProgressBar(cnt,totalMap,pctLand)
            grid = Island.ConnectToContinent(grid,rng=3)
            grid = Island.ConnectRandomPoints(grid, xmin, xmax, ymin, ymax)
            grid = Island.ChangeIsolatedPoints(grid, xmin, xmax, ymin, ymax)
            Island.ProgressBar(cnt,totalMap,pctLand)
        if itype != 0:
            world.CreateWorld(grid=Island.ConvertGrid(grid),buildings=buildings)  
        player = Player(123456,world)  
        world.AddPlayer(player)
        for i in range(enemySpawn):
            world.AddEnemy(Enemy(world))
        # console = Console(world,player,sounds)
        console.world = world
        console.player = player
        console.sounds = sounds
        ##########################################################################
    else:
        world = loadWorld(load)
        world.exit = False
        player = world.pdict["Player"][0]
        console = Console(world,player[0],sounds)
        console.world = world
        console.player = player[0]
        console.sounds = sounds
    if not simplify:
        ts = threading.Thread(target=sounds.PlayBG,args=())
        ts.start()
    
    # if firstRun:
    #     console.menu = True
    #     firstRun = False
    # else:
    #     console.menu = False


    if not simplify:
        t1 = threading.Thread(target=GetInput,args=(world,123456,console,None,))    
        t1.start()
        t2 = threading.Thread(target=console.WorldRefresh,args=(0.01,))    
        t2.start()
    else:
        console.DrawWorld()
    init = False
    while True:
        if not simplify and not console.menu:            
            world.UpdateWorld(eOnly=init,pOnly=False)
        if console.save is not None:
            saveWorld(world,console.save,console.saveMetaName) 
            console.save = None
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
    return console, world

def main():
    """
    This is the main function which runs the main game loop. It instantiates the world, player, and console.
    """
    cmd('cls')
    # random.seed(1236489)
    simplify = False #This is used for debugging purposes.
    n, enemySpawn, seed, save, load, buildings = parseInput()
    # seed = 1675142236
    if seed is None:
        seed = round(time())
    firstRun = False
    while True:
        console, world = NewWorld(n, enemySpawn, seed, save, load, buildings, simplify, firstRun)
        seed = round(time())
        load = console.load
        if world.fullExit:
            break
    world.fullExit = False
    world.exit = False
    cmd('cls')
    cmd("ECHO Thank you for playing!    ...TeeHee")
    if save is not None:
        saveWorld(world, save)
    cmd(f"ECHO {seed}")
    cmd('pause')

if __name__ == "__main__":
    main()

    
