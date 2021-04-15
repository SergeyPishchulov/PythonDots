import threading
import time

from Domain import Field
from Domain.Cycles import Cycles
from Domain.Players.PlayersConfigurator import PlayersConfigurator
from UI import PauseScreen


class Game:
    def __init__(self, ui, configurator, server):
        self.quit_flag = False
        self.ui = ui
        self.field = Field.Field(ui.width, ui.height, ui)
        self.configurator = configurator
        self.players = configurator.get_players(ui)
        self.server = server
        self.should_act = 0
        self.interrupted = False

    def run(self):
        self.ui.draw_the_canvas(self.field, self.players,
                                clear=True)
        while not self.quit_flag:
            exit_code = self.players[self.should_act].act(self.field)
            if exit_code == -1:
                self.pause()
            Cycles.find_occupied_dots(self.field)
            self.ui.draw_the_canvas(self.field, self.players)
            if self.server:
                self.server.send_update_to_remote_players(self.field)
            if not self.quit_flag:
                self.quit_flag = self.is_game_finished()
            self.should_act = (self.should_act + 1) % len(self.players)

    def pause(self):
        want_exit = PauseScreen.show(self.ui.canvas)
        if want_exit:
            self.quit_flag = True
            self.interrupted = True
        else:
            self.ui.draw_the_canvas(self.field, self.players,
                                    clear=True)

    def get_game_result(self):
        score = [p.score for p in self.players]
        if all(p == score[0] for p in score):
            return {'score': score, 'result': 'DRAW', 'winners': self.players}
        winner_score = max(score)
        winners = list(filter(lambda p: p.score == winner_score, self.players))
        return {'score': score, 'result': 'win', 'winners': winners[0]}

    def is_game_finished(self):
        return not Field.Field.ability_to_mark(self.field, self.should_act)
