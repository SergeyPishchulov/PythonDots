import random
from Domain.Players import Player


class SimpleBot(Player.Player):
    def __str__(self):
        return 'SimpleBot'

    def act(self, field):
        success = False
        while not success:
            x = random.randint(0, field.width)
            y = random.randint(0, field.height)
            success = field.mark_dot(x, y, self)
