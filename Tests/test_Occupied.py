import unittest
from Domain import  Field
from Domain.Cycles import Cycles
from Domain.Players.Player import Player


class TestOccupied(unittest.TestCase):
    def test_dot_inside_occupied_area(self):
        field = Field.Field(5, 5)
        player = Player(1, field)
        field.mark_dot(0, 1, player)  # _x
        field.mark_dot(1, 0, player)  # xzx
        field.mark_dot(2, 1, player)  # _x
        field.mark_dot(1, 2, player)  #
        Cycles.find_occupied_dots(field)
        occ_b_enm = field.field_array[1][1].occupied_by_enemy()
        self.assertTrue(occ_b_enm)

    def test_dot_outside_occupied_area_contact_with_area(self):
        field = Field.Field(5, 5)
        player = Player(1, field)
        field.mark_dot(0, 1, player)  # _x_z
        field.mark_dot(1, 0, player)  # x_x
        field.mark_dot(2, 1, player)  # _x
        field.mark_dot(1, 2, player)  #
        Cycles.find_occupied_dots(field)
        not_occ = field.field_array[3][0].occupied_by_enemy()
        self.assertFalse(not_occ)

    def test_dot_outside_occupied_area_do_not_contact_with_area(self):
        field = Field.Field(6, 6)
        player = Player(1, field)
        field.mark_dot(0, 1, player)  # _x___z
        field.mark_dot(1, 0, player)  # x_x
        field.mark_dot(2, 1, player)  # _x
        field.mark_dot(1, 2, player)  #
        _ = Cycles.find_occupied_dots(field)
        not_occ = field.field_array[5][0].occupied_by_enemy()
        self.assertFalse(not_occ)

    def test_occupied_cell_marked_as_occupied(self):
        field = Field.Field(5, 5)
        occupier = Player(1, field)
        field.mark_dot(0, 1, occupier)  # _x
        field.mark_dot(1, 0, occupier)  # xzx
        field.mark_dot(2, 1, occupier)  # _x
        field.mark_dot(1, 2, occupier)  #
        Cycles.find_occupied_dots(field)
        self.assertEqual(field.field_array[1][1].occupier, occupier)

    def test_cell_marked_as_occupied_staggered_layout_with_empty(self):
        field = Field.Field(3, 3)
        occupier = Player(1,field)
        field.mark_dot(0, 1, occupier)  # _x
        field.mark_dot(1, 0, occupier)  # xzx
        field.mark_dot(2, 1, occupier)  # _x
        field.mark_dot(1, 2, occupier)  #
        Cycles.find_occupied_dots(field)
        self.assertEqual(field.field_array[1][1].occupier, occupier)

    def test_cell_marked_as_occupied_staggered_layout_with_enemy(self):
        field = Field.Field(3, 3)
        player_x = Player(1,field)
        player_z = Player(2, field)
        field.mark_dot(0, 1, player_z)  # xzx
        field.mark_dot(1, 0, player_z)  # zxz
        field.mark_dot(2, 1, player_z)  # xzx
        field.mark_dot(1, 2, player_z)  #

        field.mark_dot(0, 0, player_x)
        field.mark_dot(0, 2, player_x)
        field.mark_dot(2, 2, player_x)
        field.mark_dot(2, 0, player_x)
        field.mark_dot(1, 1, player_x)

        Cycles.find_occupied_dots(field)
        self.assertEqual(field.field_array[1][1].occupier, player_z)
