import curses
import unittest

from Domain.Cell import Cell
from Domain.Players.Player import Player
from UI import UI


class TestUI(unittest.TestCase):
    def test_occupied_cell_without_owner(self):
        player = Player(_id=0)
        cell = Cell(0, 0, owner=None, occupier=player)
        cell.drenched = True
        color = UI.get_color_pair(cell)
        self.assertEqual(1, color)
