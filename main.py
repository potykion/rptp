import logging
import os

import rptp

logging.getLogger().setLevel(logging.INFO)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

if __name__ == '__main__':
    print('Wellcome to RPTP-2')
    print()
    print('New features:')
    print(" - Enter 'low' or 'l' to decrease actress priority")
    print()

    print('Loading actresses...')

    with rptp.ActressManager() as manager:
        actress = manager.random_actress()
        print('Randomly picked actress - {}'.format(actress['name']))

        print('Loading browser...')

        with rptp.Browser() as browser:
            browser.search_videos(actress['name'])

            command = None

            while True:
                # receive command
                if command is None:
                    command = input('Type "Enter" to search videos with another actress:\n')

                # process command
                if command == '':
                    actress = manager.random_actress()
                    print(actress['name'])
                    browser.search_videos(actress['name'])

                    command = None
                elif command in ('l', 'low'):
                    actress['priority'] -= 1

                    command = ''
                else:
                    break
