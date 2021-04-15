import curses
import itertools
from Domain.Players.PlayersConfigurator import PlayersConfigurator
from UI.ChoosePlayerScreen import ChoosePlayerScreen


def get_color_dict():
    return {0: curses.COLOR_BLACK,
            1: curses.COLOR_RED,
            2: curses.COLOR_GREEN,
            3: curses.COLOR_MAGENTA,
            4: curses.COLOR_YELLOW}


def init_color_pairs():  # цвет точки, цвет фона
    color_dict = get_color_dict()
    for (cell_color_number, background_color_number) in itertools.product(
            color_dict.keys(), color_dict.keys()):
        if (cell_color_number, background_color_number) != (0, 0):
            curses.init_pair(10 * cell_color_number + background_color_number,
                             color_dict[cell_color_number],
                             color_dict[background_color_number])


def get_color_pair(cell):
    background_color_number = 0
    if cell.drenched:
        if cell.occupied_by_smb():
            background_color_number = cell.occupier.id + 1
        else:
            background_color_number = cell.owner.id + 1
    cell_color_number = 0
    if cell.belongs_smb():
        cell_color_number = cell.owner.id + 1
    return 10 * cell_color_number + background_color_number


def print_too_little_window_exc(canvas):
    canvas.clear()
    canvas.addstr('Too little window')
    canvas.refresh()


def get_act_position(canvas):
    event = canvas.getch()
    if event == curses.KEY_MOUSE:
        _, click_x, click_y, _, _ = curses.getmouse()
        return click_x - 1, click_y - 1
    if event in (ord("q"), ord("й")):
        return -1
    else:
        return None


def fill_players_info(canvas, players, start_column=0):
    start_row = 0
    canvas.addstr(start_row, start_column, 'SCORE:')
    for i in range(len(players)):
        player = players[i]
        canvas.addstr(start_row + i + 1, start_column,
                      '   {0} : {1}'.format(player, player.score))


class UI:
    def __init__(self, canvas, w, h):
        self.canvas = canvas
        self.width = w
        self.height = h
        self.canvas.keypad(True)
        self.server = None
        curses.mousemask(True)
        curses.noecho()
        curses.start_color()
        init_color_pairs()
        # curses.raw()

    def start(self):
        configurator = PlayersConfigurator(self)
        choose_player_scr = ChoosePlayerScreen(self, configurator)
        choose_player_scr.show()

    def get_act_position(self):
        event = self.canvas.getch()
        if event == curses.KEY_MOUSE:
            _, click_x, click_y, _, _ = curses.getmouse()
            return click_x - 1, click_y - 1
        if event in (ord("q"), ord("й")):
            return -1
        else:
            return None

    def get_players_number(self):
        self.show_players_number_choose()
        while True:
            event = self.canvas.getch()
            if event in (ord("q"), ord("й")):
                break
            for i in range(2, 5):
                if event == ord(str(i)):
                    return i

    def show_players_number_choose(self):
        self.canvas.clear()
        self.canvas.addstr(11, 20, 'Press the number of players from 2 to 4')
        self.canvas.addstr(12, 20, 'Press "q" to quit')

    def draw_edges(self):
        self.canvas.addstr(0, 0, '#' * (self.width + 2))  # верхняя и нижняя
        self.canvas.addstr(self.height + 1, 0, '#' * (self.width + 2))
        for y in range(self.height + 2):  # левая и правая
            self.canvas.addstr(y, 0, '#')
            self.canvas.addstr(y, self.width + 1, '#')

    def draw_the_canvas(self, field, players, clear=False):
        if clear:
            self.canvas.clear()
        while 1:
            try:
                for x in range(field.width):
                    for y in range(field.height):
                        cell = field.field_array[x][y]
                        self.draw_the_dot(cell)
                self.draw_edges()
                fill_players_info(self.canvas, players, self.width + 2)
                self.canvas.refresh()
                break
            except curses.error:
                print_too_little_window_exc(self.canvas)

    def draw_the_dot(self, cell):
        if not cell.is_empty():
            color = curses.color_pair(get_color_pair(cell))
            self.canvas.addstr(cell.y + 1, cell.x + 1, 'x', color)
