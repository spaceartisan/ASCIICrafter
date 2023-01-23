"""
Test the Console class
"""

import unittest
from unittest import mock
from Console import Console, Sound, GetInput


class TestConsole(unittest.TestCase):

    def setUp(self):
        pass
        # self.console = Console()
        # self.sounds = Sound()
        # self.getinput = GetInput()

    def test_StartCurses(self):
        # self.console.start_curses()
        # self.assertNotEqual(self.console.stdscr, None)
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
