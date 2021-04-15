import curses

from UI import UI


def show(canvas):
    while True:
        try:
            __fil_menu(canvas)
            event = canvas.getch()
            if event in (ord("q"), ord("й")):
                return True
            if event in (ord("c"), ord("с")):
                return False
        except curses.error:
            UI.print_too_little_window_exc(canvas)


def __fil_menu(canvas):
    canvas.clear()
    canvas.addstr(11, 20, 'Press "q" to quit')
    canvas.addstr(12, 20, 'Press "c" to continue')
    canvas.refresh()
