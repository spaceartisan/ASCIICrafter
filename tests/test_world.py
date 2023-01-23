"""
Test the World class
"""


import unittest
from World import World


class TestWorld(unittest.TestCase):

    def setUp(self):
        self.world1 = World(0, 10, 0, 10)
        self.world2 = World(0, 50, 0, 50)

    def test_world1(self):
        self.assertEqual(self.world1.xmax, 10)
        self.assertEqual(self.world1.ymax, 10)
        self.assertEqual(self.world1.xmin, 0)
        self.assertEqual(self.world1.ymin, 0)
        self.assertEqual(self.world2.xmax, 50)
        self.assertEqual(self.world2.ymax, 50)
        self.assertEqual(self.world2.xmin, 0)
        self.assertEqual(self.world2.ymin, 0)

    def test_AlterWorld(self):
        self.world1.AlterWorld(0, 0, 1)
        self.assertEqual(self.world1.wmap[0][0], 1)
        self.world2.AlterWorld(self.world2.xmax-1, self.world2.ymax-1, 2)
        self.assertEqual(self.world2.wmap[self.world2.xmax-1][self.world2.ymax-1], 2)

if __name__ == '__main__':
    unittest.main()