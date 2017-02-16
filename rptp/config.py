import os

DATA_FOLDER = 'data/'
ACTRESS_BASE_PATH = DATA_FOLDER + 'actresses.json'
SESSION_BASE_PATH = DATA_FOLDER + 'sessions.json'
LOGIN_FILE = DATA_FOLDER + 'login.txt'

LOGIN = ''
PASSWORD = ''

CANT_FIND_LOGIN_STRING = 'Can\'t find VK login and pass. Please enter them like that "{}":\n'


def load_login():
    global LOGIN, PASSWORD

    login_string = 'sample_login, sample_pass'

    if os.path.exists(LOGIN_FILE):
        with open(LOGIN_FILE) as f:
            login_string = f.read()
    else:
        login_string = input(CANT_FIND_LOGIN_STRING.format(login_string)).strip(' "')
        with open(LOGIN_FILE, 'w') as f:
            f.write(login_string)

    LOGIN, PASSWORD = map(lambda login: login.strip(), login_string.split(','))


os.makedirs(DATA_FOLDER, exist_ok=True)
load_login()
