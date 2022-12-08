import sys
from argparse import ArgumentParser

from worldconv.utils import config


parser = ArgumentParser()
parser.add_argument('mode', help='Convert to: online & offline',
                    type=str, default='')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        mode: str = parser.parse_args().mode
        if not ((mode != '') and (mode == 'online' or mode == 'offline')):
            parser.print_help()
        elif not (config.load()):
            if (mode == 'online'):
                print('online')
            else:
                print('offline')
