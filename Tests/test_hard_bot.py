import unittest

from Domain.Cell import Cell
from Domain.Cycles import Cycles
from Domain.Field import Field
from Domain.Players.HardBot import HardBot
from Domain.Players.Player import Player


class TestHardBot(unittest.TestCase):

    def test_hard_occupy_single_enemy_dot(self):
        field = Field(3, 3)
        enemy = Player(0)
        field.field_array[1][1] = Cell(1, 1, enemy)
        hard_bot = HardBot(1)
        for i in range(4):
            hard_bot.act(field)
            Cycles.find_occupied_dots(field)
        self.assertEqual(field.field_array[1][0].owner, hard_bot)
        self.assertEqual(field.field_array[0][1].owner, hard_bot)
        self.assertEqual(field.field_array[2][1].owner, hard_bot)
        self.assertEqual(field.field_array[1][2].owner, hard_bot)
