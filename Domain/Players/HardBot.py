import random
from Domain.Players import Player


class HardBot(Player.Player):
    def __init__(self, __id):
        super().__init__(__id)
        self.target = None

    def __str__(self):
        return 'HardBot'

    def act(self, field):
        if self.target and self.target.occupied_by_smb():
            self.target = None

        all_cells = set(field.all_cells)
        while not self.target and all_cells:
            c = all_cells.pop()
            if not c.occupied_by_smb() and \
                    c.belongs_to_enemy(self) and \
                    all(map(lambda x: x.is_empty(),
                            field.get_4_side_neighbors(c))):
                self.target = c
                break
        if self.target and not self.target.occupied_by_smb():
            self.turn_on_target_area(field)
        else:
            self.random_turn(field)
            self.target = None

    def random_turn(self, field):
        success = False
        while not success:
            x = random.randint(0, field.width)
            y = random.randint(0, field.height)
            success = field.mark_dot(x, y, self)

    def turn_on_target_area(self, field):
        neighbors = set(field.get_4_side_neighbors(self.target))
        while neighbors:
            neighbor = neighbors.pop()
            success = field.mark_dot(neighbor.x, neighbor.y, self)
            if success:
                return
        self.random_turn(field)
        self.target = None
