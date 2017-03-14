import logging
import os

import sys
from pynput import keyboard

dir_ = os.path.dirname(os.path.realpath(__file__))
print(dir_)
os.chdir(dir_)

from rptp.texts import WELCOME_TEXT, COMMANDS
import rptp

logging.getLogger().setLevel(logging.INFO)


def on_press(key):
    global actress

    if key == keyboard.Key.esc:
        raise InterruptedError('Bye-bye!')

    elif key == keyboard.Key.enter:
        actress = manager.random_actress()
        print(actress)

        successfully = browser.search_videos(actress.name)
        if not successfully:
            raise InterruptedError('Ooops! Browser was closed!')
    elif key == keyboard.Key.space:
        actress.priority -= 1
        print('{} - priority lowered'.format(actress))
        on_press(keyboard.Key.enter)


if __name__ == '__main__':
    print(WELCOME_TEXT)
    print('Loading actresses...')

    with rptp.ActressManager() as manager:
        actress = manager.random_actress()
        print('Randomly picked actress - {}'.format(actress))

        print('Loading browser...')
        with rptp.Browser() as browser:
            browser.search_videos(actress.name)
            print(COMMANDS)

            with keyboard.Listener(on_press=on_press) as listener:
                try:
                    listener.join()
                except InterruptedError as e:
                    print(e)
                    sys.exit(0)
