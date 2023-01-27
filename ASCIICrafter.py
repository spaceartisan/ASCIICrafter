# -*- coding: utf-8 -*-
"""
ASCIICrafter
============
This is the top level main file. It is used to run the game.
Here you can configure the game's settings. This includes the world size, the world type, and the player's starting position.


"""

from os import system as cmd
from time import sleep
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

    size = 10
    enemyAmt = 1
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


def saveWorld(world, filename):
    """
    This function saves the world and player to a file.

    Parameters
    ----------
    world : World
        The world to be saved.
    filename : str
        The name of the file to be saved to.
    """
    with open(filename, "wb") as f:
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
        world = pickle.load(f)
    return world

def main():
    """
    This is the main function which runs the main game loop. It instantiates the world, player, and console.
    """
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
    n, enemySpawn, seed, save, load, buildings = parseInput()
    if seed is not None:
        random.seed(seed)
    if load is None:
        # enemySpawn = 0
        pctLand = 0.4
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
            grid = Island.AddRandomPointsToGrid(grid, rn, True, 0, 15)
            for i in range(0,6):
                grid = Island.ConnectRandomPoints(grid)
            grid = Island.ChangeIsolatedPoints(grid)
        elif itype == 2:
            grid = Island.CreateGrid(n,n)
            while True:   
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
            world.CreateWorld(grid=Island.ConvertGrid(grid),buildings=buildings)  
        player = Player(123456,world)  
        world.AddPlayer(player)
        for i in range(enemySpawn):
            world.AddEnemy(Enemy(world))
        console = Console(world,player,sounds)
        ##########################################################################
    else:
        world = loadWorld(load)
        world.exit = False
        player = world.pdict["Player"][0]
        console = Console(world,player[0],sounds)
    if not simplify:
        ts = threading.Thread(target=sounds.PlayBG,args=())
        ts.start()
    
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
    if save is not None:
        saveWorld(world, save)
    print("ASDFASDFASDF: ",buildings)
    cmd('pause')

if __name__ == "__main__":
    main()

    
