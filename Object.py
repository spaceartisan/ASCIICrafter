# -*- coding: utf-8 -*-
"""
Object
======
Object.py - This file contains the WorldObjects class and the Item class.
I think I will add enums to this file.

.. todo::   
      Add more clear enums to this file and other relevant items. Further flesh out the item class.
"""


class WorldObjects:
    """
    This class contains the objects that can be found in the world. These are the enums.
    """
    TREE = [5,0]
    FLOWER = [1,1]
    MINE = [10,2]
    SPEC = [15,3]
    def ReturnObj(objNm):
        """Returns the object based on the number.
        
        Parameters
        ----------
        objNm : int
            The number of the object.

        Returns
        -------
        WorldObjects
            The object.
        """
        if objNm == 2:
            return WorldObjects.TREE
        elif objNm == 1:
            return WorldObjects.FLOWER
        elif objNm == 3:
            return WorldObjects.MINE
        elif objNm == 4:
            return WorldObjects.SPEC

class Item:
    """
    This class contains the items that can be found in the world.
    """
    def __init__(self,world=None):
        self.world = world
        self.name = "Item"
        self.desc = "This is an item."
        self.type = "item"
        self.value = 0
        self.stack = 1
        self.maxstack = 1