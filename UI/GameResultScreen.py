import curses

from UI import UI


def show(canvas, game_result, players):
    while True:
        try:
            __fill_menu(canvas, game_result, players)
            event = canvas.getch()
            if event in (ord("q"), ord("й")):
                break
        except curses.error:
            UI.print_too_little_window_exc(canvas)


def __fill_menu(canvas, game_result, players):
    canvas.clear()
    UI.fill_players_info(canvas, players)
    if game_result['result'] == 'DRAW':
        canvas.addstr(len(players) + 3, 0, 'D R A W')
    else:
        winner = game_result['winners']
        canvas.addstr(len(players) + 3, 0, '!!! W I N !!!')
        canvas.addstr(len(players) + 4, 0, 'Winner is {0}. Score: {1}'.
                      format(winner, winner.score))
    canvas.addstr(6 + len(players), 0, 'Press "q" to quit')
    canvas.refresh()
