import unittest
from Domain import Cell
from Domain.Players.Player import Player


class TestOccupied(unittest.TestCase):
    def test_group_by_x_3_dots_in_line_horizontally(self):
        player = occupier = Player(-1)
        c1 = Cell.Cell(0, 0, player, occupier)
        c2 = Cell.Cell(1, 0, player, occupier)
        c3 = Cell.Cell(2, 0, player, occupier)
        cells = {c1, c2, c3}
        expected = {1: {c2}}
        self.assertEqual(expected, Cell.group_by_x(cells))

    def test_group_by_x_4_dots_in_line_horizontally(self):
        player = occupier = Player(-1)
        c1 = Cell.Cell(0, 0, player, occupier)
        c2 = Cell.Cell(1, 0, player, occupier)
        c3 = Cell.Cell(2, 0, player, occupier)
        c4 = Cell.Cell(3, 0, player, occupier)
        cells = {c1, c2, c3, c4}
        expected = {1: {c2}, 2: {c3}}
        self.assertEqual(expected, Cell.group_by_x(cells))

    def test_group_by_x_3_dots_in_line_vertically(self):
        player = occupier = Player(-1)
        c1 = Cell.Cell(0, 0, player, occupier)
        c2 = Cell.Cell(0, 1, player, occupier)
        c3 = Cell.Cell(0, 2, player, occupier)
        cells = {c1, c2, c3}
        expected = {}
        self.assertEqual(expected, Cell.group_by_x(cells))

    def test_3_cells_in_line_horizontally_middle(self):
        player = occupier = Player(-1)
        cell = Cell.Cell(1, 0, player, occupier)
        cells = {Cell.Cell(0, 0, player, occupier), cell, Cell.Cell(2, 0, player, occupier)}
        self.assertTrue(Cell.is_between_cells(cell, cells))

    def test_3_cells_in_line_horizontally_left(self):
        player = occupier = Player(-1)
        cell = Cell.Cell(0, 0, player, occupier)
        cells = {Cell.Cell(1, 0, player, occupier), cell, Cell.Cell(2, 0, player, occupier)}
        self.assertFalse(Cell.is_between_cells(cell, cells))

    def test_3_cells_in_line_horizontally_right(self):
        player = occupier = Player(-1)
        cell = Cell.Cell(2, 0, player, occupier)
        cells = {Cell.Cell(1, 0, player, occupier), cell, Cell.Cell(0, 0, player, occupier)}
        self.assertFalse(Cell.is_between_cells(cell, cells))

    def test_3_cells_with_gap_horizontally_middle(self):
        player = occupier = Player(-1)
        cell = Cell.Cell(1, 0, player, occupier)
        cells = {Cell.Cell(0, 0, player, occupier), cell, Cell.Cell(3, 0, player, occupier)}
        self.assertFalse(Cell.is_between_cells(cell, cells))

    def test_3_cells_with_gap_vertically_middle(self):
        player = occupier = Player(-1)
        cell = Cell.Cell(0, 1, player, occupier)
        cells = {Cell.Cell(0, 0, player, occupier), cell, Cell.Cell(0, 2, player, occupier)}
        self.assertFalse(Cell.is_between_cells(cell, cells))

    def test_belongs_to_its_owner(self):
        player = Player(-1)
        cell = Cell.Cell(0, 0, player)
        self.assertTrue(cell.belongs(player))

    def test_doesnt_belongs_to_others_owner(self):
        player = Player(1)
        other = Player(2)
        cell = Cell.Cell(0, 0, player)
        self.assertFalse(cell.belongs(other))

    def test_players_cell_is_not_enemy_cell(self):
        player = Player(1)
        cells = {Cell.Cell(0, 0, player)}
        self.assertFalse(Cell.contains_enemy(cells, player))

    def test_others_cell_is_enemy_cell(self):
        player = Player(1)
        other = Player(2)
        cells = {Cell.Cell(0, 0, player)}
        self.assertTrue(Cell.contains_enemy(cells, other))

    def test_nobodys_cell_is_not_enemys_cell(self):
        player = Player(1)
        cells = {Cell.Cell(0, 0, owner=None)}
        self.assertFalse(Cell.contains_enemy(cells, player))

    def test_raises_exception_if_owner_is_int_but_not_player_obj(self):
        player = Player(1)
        cell = Cell.Cell(0, 0, player)
        self.assertRaises(TypeError, cell.belongs, player=1)
