"""
Test the Object class
"""

import unittest
from Object import WorldObjects, Item

class TestObject(unittest.TestCase):

    def SetUp(self):
        pass

    def test_WorldObjects(self):
        self.assertEqual(WorldObjects.TREE, [5,0])
        self.assertEqual(WorldObjects.FLOWER, [1,1])
        self.assertEqual(WorldObjects.MINE, [10,2])
        self.assertEqual(WorldObjects.SPEC, [15,3])

    def test_Item(self):
        item1 = Item()
        self.assertEqual(item1.name, "Item")
        self.assertEqual(item1.desc, "This is an item.")
        self.assertEqual(item1.type, "item")
        self.assertEqual(item1.value, 0)
        self.assertEqual(item1.stack, 1)
        self.assertEqual(item1.maxstack, 1)

if __name__ == '__main__':
    unittest.main()