# -*- coding: utf-8 -*-
"""
Object.py - This file contains the WorldObjects class and the Item class.
I think I will add enums to this file.
"""


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

class Item:
    def __init__(self,world=None):
        self.world = world
        self.name = "Item"
        self.desc = "This is an item."
        self.type = "item"
        self.value = 0
        self.stack = 1
        self.maxstack = 1