from Domain import Cell
from Domain.Players.Player import Player
import copy


class Field:
    def __init__(self, w, h, drawing=None, parent_field=None):
        if parent_field is None:
            self.drawing = drawing
            self.width = w
            self.height = h
            self.field_array = []
            for x in range(self.width):
                c = [Cell.Cell(x, y) for y in range(self.height)]
                self.field_array.append(c)
        else:
            self.width = parent_field.width
            self.height = parent_field.height
            self.field_array = copy.deepcopy(parent_field.field_array)

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def mark_dot(self, x, y, player):
        if not isinstance(player, Player):
            raise ValueError()
        if not self.in_bounds(x, y) \
                or self.field_array[x][y].occupied_by_enemy(player) \
                or self.field_array[x][y].belongs_smb():
            return False
        self.field_array[x][y].owner = player
        return True

    def ability_to_mark(self, player):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.field_array[x][y]
                if not cell.belongs_smb() \
                        and not cell.occupied_by_enemy(player):
                    return True
        return False

    def get_4_side_neighbors(self, dot):
        neighbors = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if self.in_bounds(dot.x + dx, dot.y + dy) \
                        and abs(dx) + abs(dy) == 1:
                    neighbors.append(self.field_array[dot.x + dx][dot.y + dy])
        return neighbors

    def get_neighbors(self, dot):  # returns cells
        neighbors = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if self.in_bounds(dot.x + dx, dot.y + dy) \
                        and dx * dx + dy * dy != 0:
                    neighbors.append(self.field_array[dot.x + dx][dot.y + dy])
        return neighbors

    @property
    def all_cells(self):
        for x in range(self.width):
            for y in range(self.height):
                yield self.field_array[x][y]
