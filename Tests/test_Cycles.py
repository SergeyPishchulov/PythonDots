import unittest
from Domain import Cycles


class TestGetDepth(unittest.TestCase):

    def test_1(self):
        parent = {1: None, 2: 1, 3: 1, 4: 3, 5: 4}
        depth = Cycles.get_cell_depth(5, parent)
        self.assertEqual(depth, 3)

    def test_1_dot(self):
        parent = {1: None}
        depth = Cycles.get_cell_depth(1, parent)
        self.assertEqual(depth, 0)

    def test_2(self):
        parent = {1: None, 2: 1, 3: 1, 4: 3, 5: 3, 6: 2, 7: 2}
        depth1 = Cycles.get_cell_depth(5, parent)
        depth2 = Cycles.get_cell_depth(7, parent)
        self.assertEqual(depth1, 2)
        self.assertEqual(depth2, 2)

    def test_rollback(self):
        parent = {1: None, 2: 1, 3: 1, 4: 3, 5: 3, 6: 2, 7: 2}
        cell, cycle_cells = Cycles.rollback(6, parent, 2)
        self.assertEqual(cell, 1)
        self.assertEqual(cycle_cells, {6, 2})

    def test_rollback_does_not_change_source_dict(self):
        parent = {1: None, 2: 1, 3: 1, 4: 3, 5: 3, 6: 2, 7: 2}
        parent_copy = parent.copy()
        cell, cycle_cells = Cycles.rollback(6, parent, 2)
        self.assertEqual(parent, parent_copy)

    def test_rollback_2_dots(self):
        parent = {1: None, 2: 1}
        cell, cycle_cells = Cycles.rollback(2, parent, 1)
        self.assertEqual(cell, 1)
        self.assertEqual(cycle_cells, {2})

    def test_rollback_1_dot(self):
        parent = {1: None}
        cell, cycle_cells = Cycles.rollback(1, parent, 1)
        self.assertEqual(cell, None)
        self.assertEqual(cycle_cells, {1})

    def test_rollback_3_dots(self):
        parent = {1: None, 2: 1, 3: 2}
        cell, cycle_cells = Cycles.rollback(3, parent, 2)
        self.assertEqual(cell, 1)
        self.assertEqual(cycle_cells, {2, 3})

    def test_rollback_empty_dict(self):
        self.assertRaises(ValueError, Cycles.rollback,
                          cell=1, parents={}, count=1)
