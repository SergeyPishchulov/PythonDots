from UI import UI
import argparse
import curses


def main():
    default_size = 16
    parser = argparse.ArgumentParser(description='Game "Dots"')
    parser.add_argument(
        '--width',
        type=int,
        default=default_size,
        help=f"takes width of field as integer (default: {default_size})"
    )

    parser.add_argument(
        '--height',
        type=int,
        default=default_size,
        help=f"takes height of field as integer (default: {default_size})"
    )

    args = parser.parse_args()
    curses.wrapper(launch, args)


def launch(scr, args):
    ui = UI.UI(scr, args.width, args.height)
    ui.start()


if __name__ == '__main__':
    main()
