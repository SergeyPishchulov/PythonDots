import curses

from Domain import Game
from UI import GameResultScreen, UI


class ChooseOpponentsScreen:
    def __init__(self, ui, configurator):
        self.ui = ui
        self.canvas = ui.canvas
        self.configurator = configurator

    def show(self):
        want_exit = self.handle_actions()
        if want_exit:
            return
        game = Game.Game(self.ui, self.configurator, self.configurator.server)
        game.run()
        if not game.interrupted:
            game_result = game.get_game_result()
            GameResultScreen.show(self.canvas, game_result, game.players)
        game.configurator.clear()

    def handle_actions(self):
        while True:
            try:
                self.__fill_menu()
                # self.show_connected_network_opponents()
                event = self.canvas.getch()
                if event in (ord("m"), ord("ь")):
                    self.configurator.add_human()
                elif event in (ord("s"), ord("ы")):
                    self.configurator.add_simple_bot()
                elif event in (ord("h"), ord("р")):
                    self.configurator.add_hard_bot()
                elif event in (ord("r"), ord("к")):
                    break
                elif event in (ord("q"), ord("й")):
                    return True
            except curses.error:
                UI.print_too_little_window_exc(self.canvas)

    def __fill_menu(self):
        self.canvas.clear()
        self.canvas.addstr(11, 10,
                           'Choose your opponents')
        self.canvas.addstr(13, 10, 'Press "m" if Human will play')
        self.canvas.addstr(14, 10, 'Press "s" if Simple Bot will play')
        self.canvas.addstr(15, 10, 'Press "h" if HARD Bot will play')

        self.canvas.addstr(18, 10, 'Press "r" to run the game')
        self.canvas.addstr(19, 10, 'Press "q" to quit')
        self.canvas.refresh()
