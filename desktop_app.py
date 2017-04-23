import argparse

from rptp.desktop.mode import change_mode

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Welcome to RPTP - app for watching VK videos with random pornstar.'
    )

    parser.add_argument(
        '-m', '--mode',
        choices=['video', 'report'], default='video',
        help='Program mode: video watch / report generation / etc.'
    )

    args = parser.parse_args()

    change_mode(args.mode)
