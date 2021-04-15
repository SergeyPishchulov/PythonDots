from Domain.Players.Bot import SimpleBot
from Domain.Players.HardBot import HardBot
from Domain.Players.Player import Player


class PlayersConfigurator:
    def __init__(self, ui):
        self.players = []
        self.server = None
        self.ui = ui

    def clear(self):
        self.players = []
        self.server = None

    @property
    def next_number(self):
        return len(self.players)

    def add_human(self):
        self.players.append(Player(self.next_number, None, self.ui))

    def add_simple_bot(self):
        self.players.append(SimpleBot(self.next_number))

    def add_hard_bot(self):
        self.players.append(HardBot(self.next_number))

    def get_players(self, ui):
        for p in self.players:
            p.ui = ui
        return self.players
