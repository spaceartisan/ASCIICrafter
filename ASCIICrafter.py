# -*- coding: utf-8 -*-
"""
ASCIICrafter
============
ASCIICrafter - A simple ASCII game engine
This is the top level main file. It is used to run the game.


"""

from os import system as cmd
from time import sleep
import threading

from Console.Console import Console, Sound, GetInput
from Entities import Player, Enemy
from World import World, Island
   

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

if __name__ == "__main__":
    main()

    
