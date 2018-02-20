import os

from rptp.app import app

if __name__ == '__main__':
    app.run(os.getenv('HOST', 'localhost'))
