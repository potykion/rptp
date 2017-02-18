import logging
import os

import rptp

TYPE_TEXT = 'Type "Enter" to search videos with another actress or type one of the commands (e.g. \'l\')\n'

logging.getLogger().setLevel(logging.INFO)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

if __name__ == '__main__':
    print('Welcome to RPTP-2')
    print()
    print('New features:')
    print(" - Enter 'low' or 'l' to decrease actress priority")
    print()

    print('Loading actresses...')

    with rptp.ActressManager() as manager:
        actress = manager.random_actress()
        print('Randomly picked actress - {}'.format(actress))

        print('Loading browser...')

        with rptp.Browser() as browser:
            browser.search_videos(actress.name)

            command = None

            while True:
                if command is None:
                    command = input(TYPE_TEXT)

                if command == '':
                    actress = manager.random_actress()
                    print(actress)
                    successfully = browser.search_videos(actress.name)
                    if not successfully:
                        print('Ooops! Browser was closed!')
                        break
                elif command in ('l', 'low'):
                    actress.priority -= 1
                else:
                    break

                command = None
