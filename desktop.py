import logging
import sys

from pynput import keyboard

from rptp.browser import Browser
from rptp.config import PICK_ON_START
from rptp.data.texts import WELCOME_TEXT, COMMANDS
from rptp.models.actress import ActressManager

logging.getLogger().setLevel(logging.INFO)


def on_press(key):
    global actress
    # if key == keyboard.Key.esc:
    #     raise InterruptedError('Bye-bye!')

    if key == keyboard.Key.enter:
        actress = manager.random_pick()
        print(actress)
        browser.request_videos(actress.name)

        if not browser.is_alive():
            raise InterruptedError('Oops, browser was closed!')

    elif key == keyboard.Key.space:
        actress.priority -= 1
        print('{} - priority lowered'.format(actress))
        on_press(keyboard.Key.enter)


if __name__ == '__main__':
    print(WELCOME_TEXT)

    print('Loading actresses...')
    with ActressManager() as manager:
        print('Loading browser...')
        with Browser() as browser:
            print(COMMANDS)

            if PICK_ON_START:
                actress = manager.random_pick()
                print('Randomly picked actress - {}'.format(actress))
                browser.request_videos(actress.name)

            with keyboard.Listener(on_press=on_press) as listener:
                try:
                    listener.join()
                except InterruptedError as e:
                    print(e)
                    sys.exit(0)
