from Domain.Players.Player import Player


def mark_each_cell_as_occupied(cells, occupier):
    for c in cells:
        if isinstance(c, Cell):
            c.occupier = occupier
            if c.belongs_to_enemy(occupier):
                occupier.occupied_dots.add(c)
        else:
            raise TypeError("unknown type" + str(type(c)))


def group_by_x(cells):
    dots_on_vertical = {}
    for cell in cells:
        if is_between_cells(cell, cells):
            if cell.x not in dots_on_vertical:
                dots_on_vertical[cell.x] = set()
            dots_on_vertical[cell.x].add(cell)
    return dots_on_vertical


def is_between_cells(cell, cells):
    has_left = any(n.x == cell.x - 1 and abs(n.y - cell.y) <= 1
                   for n in cells)
    has_right = any(n.x == cell.x + 1 and abs(n.y - cell.y) <= 1
                    for n in cells)
    return has_left and has_right


def bounds(cells_on_vertical):
    upper = max(cells_on_vertical, key=lambda c: c.y).y
    lower = min(cells_on_vertical, key=lambda c: c.y).y
    return upper, lower


def flatten(collection):
    res = set()
    for c in collection:
        for i in c:
            res.add(i)
    return res


def contains_by_y(cells, y):
    return any(c.y == y for c in cells)


def contains_enemy(cells, player):
    return any(
        cell.owner != player and cell.owner is not None for cell in cells)


def contains_by_cell(cells, cell):
    return any(item.equals(cell) for item in cells)


class Cell:
    def __init__(self, x, y, owner=None, occupier=None):
        self.x = x
        self.y = y
        self.owner = owner
        self.occupier = occupier
        self.drenched = False

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, new_owner):
        if isinstance(new_owner, Player) or new_owner is None:
            self._owner = new_owner
        else:
            raise ValueError('expected instance of Player')

    @property
    def occupier(self):
        return self._occupier

    @occupier.setter
    def occupier(self, new_occupier):
        if isinstance(new_occupier, Player) or new_occupier is None:
            self._occupier = new_occupier
        else:
            raise ValueError('expected instance of Player')

    def equals(self, another):
        if isinstance(another, Cell):
            return self.x == another.x and self.y == another.y
        raise TypeError('Equals supported only between 2 Cells')

    def belongs(self, player):
        if isinstance(player, Player):
            return self.owner == player
        raise TypeError('expected instance of Player')

    def belongs_smb(self):
        return self.owner is not None

    def belongs_to_enemy(self, player):
        return self.belongs_smb() and not self.belongs(player)

    def is_empty(self):
        return not self.belongs_smb() and not self.occupied_by_smb()

    def occupied_by_enemy(self, player=None):
        if player is None:
            player = self.owner
        return self.occupied_by_smb() and self.occupier != player

    def occupied_by_smb(self):
        return self.occupier is not None

    def __str__(self):
        return 'x:{0}, y:{1}'.format(self.x, self.y)

    def __repr__(self):
        return '({},{})'.format(self.x, self.y)
