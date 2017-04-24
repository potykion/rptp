import logging
import sys

from pynput import keyboard

from rptp.browser import Browser
from rptp.config import PICK_ON_START
from rptp.desktop.data.texts import COMMANDS
from rptp.models.actress import ActressManager

logging.getLogger().setLevel(logging.INFO)

state = {}


def on_press(key):
    global state

    if key == keyboard.Key.enter:
        actress = state['actresses'].random_pick()
        print(actress)
        state['browser'].request_videos(actress.name)

        if not state['browser'].is_alive():
            raise InterruptedError('Oops, browser was closed!')

    elif key == keyboard.Key.space:
        state['actress'].priority -= 1
        print('{} - priority lowered'.format(state['actress']))
        on_press(keyboard.Key.enter)


def start_watch_videos():
    global state

    print('Loading actresses...')
    with ActressManager() as manager:
        state['actresses'] = manager

        print('Loading browser...')
        with Browser() as browser:
            state['browser'] = browser

            print(COMMANDS)

            if PICK_ON_START:
                actress = manager.random_pick()
                state['actress'] = actress

                print('Randomly picked actress - {}'.format(actress))
                browser.request_videos(actress.name)

            with keyboard.Listener(on_press=on_press) as listener:
                try:
                    listener.join()
                except InterruptedError as e:
                    print(e)
                    sys.exit(0)
