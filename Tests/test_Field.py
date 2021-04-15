import unittest

from Domain import Cycles, Field
from Domain.Players.Player import Player


def is_empty(field):
    res = True
    for x in range(field.width):
        for y in range(field.height):
            res = res and not field.field_array[x][y].belongs_smb()
    return res


class TestMarkDots(unittest.TestCase):

    def test_can_mark_dot(self):
        field = Field.Field(5, 5)
        player = Player(1, field)
        field.mark_dot(2, 3, player)
        self.assertEqual(field.field_array[2][3].owner, player)

    def test_can_not_mark_dot_in_already_marked_cell(self):
        field = Field.Field(5, 5)
        player = Player(1, field)
        another = Player(2,field)
        field.mark_dot(0, 0, player)
        field.mark_dot(0, 0, another)
        self.assertEqual(field.field_array[0][0].owner, player)

    def test_can_not_mark_at_the_edge(self):
        field = Field.Field(5, 5)
        player = Player(1, field)
        field.mark_dot(-1, -1, player)
        field.mark_dot(5, 5, player)
        field.mark_dot(-1, 5, player)
        field.mark_dot(5, -1, player)
        self.assertTrue(is_empty(field))

    def test_can_mark_dot_inside_its_own_occupied_area(self):
        field = Field.Field(5, 5)
        player = Player(1, field)
        field.mark_dot(0, 1, player)  # _x
        field.mark_dot(1, 0, player)  # xzx
        field.mark_dot(2, 1, player)  # _x
        field.mark_dot(1, 2, player)  #
        Cycles.find_occupied_dots(field)
        success = field.mark_dot(1, 1, player)
        self.assertTrue(success)

    def test_can_not_mark_dot_inside_others_occupied_area(self):
        field = Field.Field(5, 5)
        player = Player(1, field)
        field.mark_dot(0, 1, player)  # _x
        field.mark_dot(1, 0, player)  # xzx
        field.mark_dot(2, 1, player)  # _x
        field.mark_dot(1, 2, player)  #
        Cycles.find_occupied_dots(field)
        success = field.mark_dot(1, 1, Player(2,field))
        self.assertFalse(success)

    def test_belongs(self):
        field = Field.Field(5, 5)
        player = Player(1, field)
        field.mark_dot(0, 1, player)  # _x
        field.mark_dot(1, 0, player)  # xzx
        field.mark_dot(2, 1, player)  # _x
        field.mark_dot(1, 2, player)  #
        actually = field.field_array[1][1].belongs_smb()
        self.assertFalse(actually)


if __name__ == '__main__':
    unittest.main()
