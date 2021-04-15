import curses

from UI import UI
from UI.ChooseOpponentsScreen import ChooseOpponentsScreen


class ChoosePlayerScreen:
    def __init__(self, ui, configurator):
        self.canvas = ui.canvas
        self.configurator = configurator
        self.choose_opp_scr = ChooseOpponentsScreen(ui, configurator)

    def show(self):
        while True:
            try:
                self.__fill_menu()
                event = self.canvas.getch()
                if event in (ord("m"), ord("ь")):
                    self.configurator.add_human()
                    self.choose_opp_scr.show()
                elif event in (ord("s"), ord("ы")):
                    self.configurator.add_simple_bot()
                    self.choose_opp_scr.show()
                elif event in (ord("h"), ord("р")):
                    self.configurator.add_hard_bot()
                    self.choose_opp_scr.show()
                if event in (ord("q"), ord("й")):
                    curses.endwin()
                    exit()
            except curses.error:
                UI.print_too_little_window_exc(self.canvas)

    def __fill_menu(self):
        self.canvas.clear()
        try:
            self.canvas.addstr(11, 10,
                               'Who will play on THIS computer?')
            self.canvas.addstr(13, 10,
                               'Press "m" if YOU will play')
            self.canvas.addstr(14, 10, 'Press "s" if Simple Bot will play')
            self.canvas.addstr(15, 10, 'Press "h" if HARD Bot will play')
            s = "Press 'c' if you want to connect to someone's game by network"
            self.canvas.addstr(16, 10, s)
            self.canvas.refresh()
        except curses.error:
            UI.print_too_little_window_exc(self.canvas)
