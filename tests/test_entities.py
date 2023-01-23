"""
Test the Entity class
"""

import unittest
from Entities import Enemy, Player

class TestEntity(unittest.TestCase):

    def setUp(self):
        pass

    def test_Enemy(self):
        enemy = Enemy()
        self.assertEqual(enemy.hp, 0)
        self.assertEqual(enemy.spd, 2)
        self.assertEqual(enemy.lastDir, 0)
        self.assertEqual(enemy.radius, 10)
        self.assertEqual(enemy.delay, 1)
        self.assertEqual(enemy.dcount, 0)

    def test_Player(self):
        player = Player()
        self.assertEqual(player.hp, 10)
        self.assertEqual(player.axe, 0)
        self.assertEqual(player.paxe, 0)
        self.assertEqual(player.swrd, 0)
        self.assertEqual(player.ids, None)
        self.assertEqual(player.px, None)
        self.assertEqual(player.py, None)
        self.assertEqual(player.harvest, False)
        self.assertEqual(player.hstats, None)
        self.assertEqual(player.cooldown, [False, False])
        self.assertEqual(player.consoleMsg, None)

if __name__ == '__main__':
    unittest.main()
